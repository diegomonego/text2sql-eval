"""Generator presets (coverage / natural), the free-form quota, and the per-run selection diagnostics."""

import json

import pytest

from t2s_eval import generator
from t2s_eval.config import PoolSettings, Preset
from t2s_eval.diagnostics import best_subset, objective, selection_diagnostics
from t2s_eval.selection import GainSettings, NotEnoughCandidates, Scored, greedy_select
from t2s_eval.targets import build_targets

G = GainSettings(weights={"a": 1.0, "b": 0.5}, repeat_penalty=0.5, lambda_shape=0.5, lambda_table=0.25,
                 lambda_column=0.25, n_tables=4, n_columns=10)


def _c(cid, tables, columns, shapes, target):
    return Scored(cid, frozenset(tables), frozenset(columns), frozenset(shapes), {"target": target})


def test_presets_load_and_validate(project):
    assert project.default_preset == "coverage"
    nat = project.get_preset("natural")
    assert (nat.free_per_n, nat.focus_tables, nat.min_free_share, nat.max_shapes, nat.alpha, nat.beta) == (2, False, 0.2, 2, 0.6, 0.4)
    assert project.pool_for(nat).free_per_n == 2 and project.pool_for(project.get_preset()).free_per_n == 1
    with pytest.raises(ValueError, match="unknown preset"):
        project.get_preset("nope")
    with pytest.raises(ValueError, match="both alpha and beta"):
        Preset("x", alpha=0.5)
    with pytest.raises(ValueError, match="style"):
        Preset("x", style="fancy")


def test_targets_can_name_a_shape_only(card):
    shapes = ["lookup", "aggregation", "ranking"]
    targets = build_targets(5, shapes, card, PoolSettings(free_per_n=2), focus_tables=False)
    targeted = [t for t in targets if t["kind"] == "targeted"]
    assert targeted and all("focus_table" not in t for t in targeted)
    assert sum(t["kind"] == "free" for t in targets) == 10


def test_quota_forces_free_form_picks():
    big = _c("t1", {"x", "y"}, {"c1", "c2"}, {"a"}, "t01")
    mid = _c("t2", {"z"}, {"c3"}, {"b"}, "t02")
    free = _c("f1", {"x"}, {"c1"}, {"a"}, "f01")
    is_free = lambda c: c.extra["target"].startswith("f")
    picks, log = greedy_select([big, mid, free], 2, G)
    assert [p.id for p in picks] == ["t1", "t2"]  # without the quota the free one loses
    picks, log = greedy_select([big, mid, free], 2, G, min_quota=1, in_quota=is_free)
    assert [p.id for p in picks] == ["t1", "f1"] and log[1]["restricted_to_quota"]
    with pytest.raises(NotEnoughCandidates, match="free-form"):
        greedy_select([big, mid], 2, G, min_quota=1, in_quota=is_free)


def test_objective_equals_the_sum_of_greedy_gains_and_exact_best():
    cands = [_c("p", {"x", "y"}, {"c1"}, {"a"}, "t01"), _c("q", {"y"}, {"c2", "c3"}, {"a", "b"}, "t02"),
             _c("r", {"z"}, {"c4"}, {"b"}, "t03"), _c("s", {"w"}, set(), {"a"}, "t04")]
    picks, log = greedy_select(cands, 2, G)
    assert objective(picks, G) == pytest.approx(sum(r["gain"]["total"] for r in log), abs=1e-5)
    res = best_subset(cands, picks, G)
    assert res["method"].startswith("exact") and res["greedy_over_best"] <= 1.0
    assert res["best_value"] >= res["greedy_value"]


NATURAL_CANDIDATES = [
    # 4 tables -> multi_join is derived: lookup + multi_join = 2 shapes, allowed
    {"target": "t01", "question": "Which customers in Europe placed orders in 1996?", "links": [
        {"phrase": "customers", "kind": "table", "table": "customer"},
        {"phrase": "Europe", "kind": "column", "columns": ["region.r_name"], "value": "EUROPE"},
        {"phrase": "in 1996", "kind": "column", "columns": ["orders.o_orderdate"], "value": "1996"},
        {"phrase": "Which", "kind": "shape", "shape": "lookup"}]},
    # ranking + aggregation + derived multi_join = 3 shapes: dropped by the natural preset's cap
    {"target": "t02", "question": "Which 5 customers in Europe had the highest total order value?", "links": [
        {"phrase": "customers", "kind": "table", "table": "customer"},
        {"phrase": "Europe", "kind": "column", "columns": ["region.r_name"], "value": "EUROPE"},
        {"phrase": "highest", "kind": "shape", "shape": "ranking"},
        {"phrase": "total", "kind": "shape", "shape": "aggregation"},
        {"phrase": "order value", "kind": "column", "columns": ["orders.o_totalprice"]}]},
    {"target": "t03", "question": "What is the total order value per market segment?", "links": [
        {"phrase": "total", "kind": "shape", "shape": "aggregation"},
        {"phrase": "order value", "kind": "column", "columns": ["orders.o_totalprice"]},
        {"phrase": "market segment", "kind": "column", "columns": ["customer.c_mktsegment"]}]},
    # free-form, low gain: picked only because of the quota
    {"target": "f01", "question": "How many customers do we have?", "links": [
        {"phrase": "How many", "kind": "shape", "shape": "aggregation"},
        {"phrase": "customers", "kind": "table", "table": "customer"}]},
]


def test_natural_preset_end_to_end(project, tmp_path):
    out = tmp_path / "run"
    msg = generator.prepare(project, 2, out, no_docs=False, anchor_setting=None, preset_name="natural")
    assert "natural preset" in msg
    brief = (out / "generation" / "brief.md").read_text()
    assert "## Preset" in brief and "ticket or a chat message" in brief and "At most 2 shapes" in brief
    targets = json.loads((out / "generation" / "targets.json").read_text())
    assert all("focus_table" not in t for t in targets) and sum(t["kind"] == "free" for t in targets) == 4
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": NATURAL_CANDIDATES}))
    code, msg = generator.select(project, out)
    assert code == 0, msg
    pool = {c["id"]: c for c in json.loads((out / "generation" / "pool.json").read_text())["candidates"]}
    assert pool["c002"]["status"] == "dropped" and "allows at most 2" in pool["c002"]["reason"]
    assert pool["c004"]["status"] == "selected"  # the free-form one, forced in by the quota
    diag = json.loads((out / "generation" / "diagnostics.json").read_text())
    assert diag["preset"] == "natural" and diag["free_form"]["picks"] >= 1 and diag["free_form"]["required"] == 1
    assert diag["greedy_vs_best"]["method"].startswith("exact")
    assert set(diag["sensitivity_picks_changed"]) >= {"lambdas in equal thirds", "W = F x I / 9 (multiplied, not added)"}
    run = json.loads((out / "generation" / "run.json").read_text())
    assert run["input"]["preset"]["name"] == "natural"
    log = json.loads((out / "generation" / "pick_log.json").read_text())
    assert (log["settings"]["alpha"], log["settings"]["beta"]) == (0.6, 0.4)


def test_coverage_preset_keeps_v1_brief_and_targets(project, tmp_path):
    out = tmp_path / "run"
    generator.prepare(project, 2, out, no_docs=False, anchor_setting=None)
    brief = (out / "generation" / "brief.md").read_text()
    assert "**coverage**" in brief and "as many different columns as possible" in brief
    targets = json.loads((out / "generation" / "targets.json").read_text())
    assert all("focus_table" in t for t in targets if t["kind"] == "targeted")
    assert sum(t["kind"] == "free" for t in targets) == 2


def test_db_and_docs_can_be_given_as_arguments(project, tmp_path, mini_db_path):
    """--db and --docs override the config; gen-select reuses what gen-prepare was given."""
    from dataclasses import replace

    from .test_pipeline_steps import CANDIDATES

    cfg = replace(project, db_url="duckdb:///does/not/exist.duckdb")  # the config's own database is unusable
    other_docs = tmp_path / "other_docs"
    other_docs.mkdir()
    (other_docs / "terms.md").write_text("# Terms\n\nOrder value = o_totalprice.\n")
    out = tmp_path / "run"
    generator.prepare(cfg, 2, out, no_docs=False, anchor_setting=None, db_url=f"duckdb:///{mini_db_path}", docs=str(other_docs))
    settings = json.loads((out / "generation" / "settings.json").read_text())
    assert settings["db_url"] == f"duckdb:///{mini_db_path}" and settings["docs_dir"] == str(other_docs)
    assert str(other_docs / "terms.md") in (out / "generation" / "brief.md").read_text()  # outside the repo: absolute path
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": CANDIDATES}))
    code, msg = generator.select(cfg, out)
    assert code == 0, msg
    run = json.loads((out / "generation" / "run.json").read_text())
    assert run["docs"][0]["path"] == str(other_docs / "terms.md")
    with pytest.raises(ValueError, match="can't be combined"):
        generator.prepare(cfg, 2, out, no_docs=True, anchor_setting=None, docs=str(other_docs))
    with pytest.raises(ValueError, match="not a directory"):
        generator.prepare(cfg, 2, out, no_docs=False, anchor_setting=None, docs=str(tmp_path / "missing"))
