# Text-to-SQL question generation and judging. Run `make help` for targets.
# Headless runs use `claude -p`, which can't answer permission prompts, so the tools each skill
# needs are pre-approved here: reading files, writing under the run folder, and `uv run t2s ...`.

SHELL := /bin/bash
CLAUDE ?= claude
CLAUDE_FLAGS ?= --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Bash(uv run t2s *)" --output-format json
N ?= 5
# New runs go to runs/new_nN by default, so reproducing never overwrites the saved runs.
RUN ?= runs/new_n$(N)
BENCHMARK ?= tpch
SF ?= 0.1
DB ?= data/tpch_sf01.duckdb
GEN_ARGS ?=
# Generator preset from config/eval.toml [presets]; empty = the config's default (coverage).
PRESET ?=
# Another config file (e.g. another database): CONFIG=config/eval_tpcds.toml. Passed to every command
# and, through the environment, to the `uv run t2s` calls the skills make.
CONFIG ?=
ifneq ($(CONFIG),)
export T2S_CONFIG := $(CONFIG)
endif
JUDGE_ARGS ?=
# Judges must work from question text alone: the Read tool is denied on any questions.json
# (the prepare step reads it through code and hands the LLM a copy with ids and texts only).
JUDGE_FLAGS ?= --disallowedTools "Read(**/questions.json)"

.PHONY: help setup db docs test skills generate judge-correctness judge-coverage judges pipeline check-run

help:
	@echo "make setup                 install Python 3.12 and dependencies (uv)"
	@echo "make db [SF=0.1]           build the TPC-H database with DuckDB (BENCHMARK=tpcds SF=0.01 DB=... for others)"
	@echo "make docs                  download the TPC-H spec and extract the sections given to the agents"
	@echo "make test                  run the self-tests (no LLM calls)"
	@echo "make skills                copy each component's model from config/eval.toml into its skill"
	@echo "make generate N=5          generate N questions into runs/new_n5 (RUN=..., PRESET=..., GEN_ARGS=...)"
	@echo "make generate N=5 PRESET=natural RUN=runs/n5_natural   use another generator preset"
	@echo "make generate N=5 CONFIG=config/eval_tpcds.toml RUN=runs/tpcds_n5 GEN_ARGS=--no-docs   another database"
	@echo "make generate N=5 GEN_ARGS='--db duckdb:///path/to.duckdb --docs path/to/docs'   inputs as arguments"
	@echo "make judges RUN=runs/x     run both judges on RUN/questions.json (JUDGE_ARGS='--no-docs' etc.)"
	@echo "make pipeline N=5          generate, judge and check one run"
	@echo "make check-run RUN=runs/x  check that the files of a run agree"

setup:
	uv sync

db:
	uv run t2s db-build --benchmark $(BENCHMARK) --sf $(SF) --out $(DB)

docs:
	uv run t2s fetch-spec

test:
	uv run pytest -q

# config/eval.toml sets each component's model; every target that runs a skill syncs first.
skills:
	uv run t2s sync-skills

generate: skills
	mkdir -p $(RUN)/logs
	$(CLAUDE) -p "/generate-questions --n $(N) --out $(RUN) $(if $(PRESET),--preset $(PRESET)) $(GEN_ARGS)" $(CLAUDE_FLAGS) > $(RUN)/logs/generator.json

judge-correctness: skills
	mkdir -p $(RUN)/logs
	$(CLAUDE) -p "/judge-correctness --questions $(RUN)/questions.json --out $(RUN) $(JUDGE_ARGS)" $(CLAUDE_FLAGS) $(JUDGE_FLAGS) > $(RUN)/logs/correctness.json

judge-coverage: skills
	mkdir -p $(RUN)/logs
	$(CLAUDE) -p "/judge-coverage --questions $(RUN)/questions.json --out $(RUN) $(JUDGE_ARGS)" $(CLAUDE_FLAGS) $(JUDGE_FLAGS) > $(RUN)/logs/coverage.json

judges: judge-correctness judge-coverage

pipeline: generate judges check-run

check-run:
	uv run t2s check-run $(RUN)
