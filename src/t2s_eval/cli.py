"""Command line: `uv run t2s <command>`. The skills call these commands; so can people."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import load_config


def _positive_int(s: str) -> int:
    v = int(s)
    if v < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return v


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="t2s", description="Question generation and judges for Text-to-SQL evaluation")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("db-build", help="build a benchmark database with DuckDB's generator")
    b.add_argument("--benchmark", choices=["tpch", "tpcds"], default="tpch")
    b.add_argument("--sf", type=float, default=0.1)
    b.add_argument("--out", required=True)

    sub.add_parser("db-info", help="connect to the configured database and print its schema card summary")
    sub.add_parser("fetch-spec", help="download the TPC-H spec and extract the sections given to the agents")

    a = sub.add_parser("anchor", help="show how the time anchor resolves")
    a.add_argument("--anchor", default=None)

    g = sub.add_parser("gen-prepare", help="generator step 1: schema card, targets and brief")
    g.add_argument("--n", type=_positive_int, required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--no-docs", action="store_true")
    g.add_argument("--anchor", default=None, help="auto | off | YYYY-MM-DD (default: config)")

    s = sub.add_parser("gen-select", help="generator step 2: check, dedupe and select exactly N")
    s.add_argument("--out", required=True)

    jp = sub.add_parser("judge-prepare", help="judge step 1: clean questions, schema card and brief")
    jp.add_argument("--judge", choices=["correctness", "coverage"], required=True)
    jp.add_argument("--questions", required=True)
    jp.add_argument("--out", required=True)
    jp.add_argument("--no-docs", action="store_true")
    jp.add_argument("--anchor", default=None)

    jf = sub.add_parser("judge-finalize", help="judge step 2: check links, compute scores, write reports")
    jf.add_argument("--judge", choices=["correctness", "coverage"], required=True)
    jf.add_argument("--questions", required=True)
    jf.add_argument("--out", required=True)
    jf.add_argument("--accept-issues", action="store_true")

    c = sub.add_parser("check-run", help="check that the files of a run folder agree")
    c.add_argument("folder")

    sk = sub.add_parser("sync-skills", help="copy each component's model from config/eval.toml into its skill")
    sk.add_argument("--check", action="store_true", help="only report skills that differ from the config")

    args = p.parse_args(argv)
    cfg = load_config()
    code, msg = 0, ""

    if args.cmd == "db-build":
        from .build import build_database

        msg = build_database(args.benchmark, args.sf, cfg.resolve(args.out))
    elif args.cmd == "fetch-spec":
        from .build import fetch_spec

        msg = fetch_spec(cfg)
    elif args.cmd == "db-info":
        from .db import connect
        from .schema_card import build_schema_card

        db = connect(cfg.db_url, cfg.root)
        card = build_schema_card(db, cfg.max_listed_values)
        notes = [f"{t['name']}.{c['name']}: {', '.join(c['notes'])}" for t in card["tables"] for c in t["columns"] if c["notes"]]
        msg = json.dumps(
            {"database": db.fingerprint(), "tables": {t["name"]: t["rows"] for t in card["tables"]},
             "joins": [f"{e['from']} -> {e['to']} ({e['source']})" for e in card["joins"]], "notes": notes},
            indent=2,
        )
    elif args.cmd == "anchor":
        from .anchor import render_anchor_md, resolve_anchor
        from .db import connect

        db = connect(cfg.db_url, cfg.root)
        msg = render_anchor_md(resolve_anchor(args.anchor or cfg.anchor_mode, cfg.anchor_column, db))
    elif args.cmd == "gen-prepare":
        from .generator import prepare

        msg = prepare(cfg, args.n, cfg.resolve(args.out), args.no_docs, args.anchor)
    elif args.cmd == "gen-select":
        from .generator import select

        code, msg = select(cfg, cfg.resolve(args.out))
    elif args.cmd == "judge-prepare":
        from .judges import prepare as jprepare

        msg = jprepare(cfg, args.judge, cfg.resolve(args.questions), cfg.resolve(args.out), args.no_docs, args.anchor)
    elif args.cmd == "judge-finalize":
        from .judges import finalize

        code, msg = finalize(cfg, args.judge, cfg.resolve(args.questions), cfg.resolve(args.out), args.accept_issues)
    elif args.cmd == "check-run":
        from .check_run import check_run

        code, msg = check_run(cfg.resolve(args.folder))
    elif args.cmd == "sync-skills":
        from .skills import sync_skills

        in_sync, lines = sync_skills(cfg, check=args.check)
        code, msg = (1 if args.check and not in_sync else 0), "Skill models:\n" + "\n".join(f"  {l}" for l in lines)
    print(msg)
    sys.exit(code)


if __name__ == "__main__":
    main()
