"""Starting values for the shape legend's I from BIRD Mini-Dev's human difficulty labels.

BIRD: Li, J., Hui, B., Qu, G., et al. (2023). Can LLM Already Serve as A Database Interface? A BIg Bench for
Large-Scale Database Grounded Text-to-SQLs. NeurIPS 2023 Datasets and Benchmarks. https://arxiv.org/abs/2305.03111
(difficulty rubric: Appendix B.1).

Offline calibration only. It reads BIRD's *existing* gold SQL to tag each question with our shapes;
the generator and judges never see or produce SQL.

Method:
1. Tag each of the 500 questions with our 8 shapes, by rules over BIRD's gold SQL (sqlglot, SQLite dialect)
   plus a few wording cues where SQL alone can't tell (ratio vs. average, period comparisons).
2. Regress BIRD's difficulty (simple=1, moderate=2, challenging=3) on the shape indicators:
       difficulty = b0 + sum_s b_s * has_s
   lookup is the baseline (a question with no other operation), so I_lookup = b0 and I_s = b0 + b_s:
   the predicted difficulty of a question with just that shape.
3. Bootstrap the questions for 95% intervals.
4. Map to the legend's 1-3 scale. BIRD gives *relative* difficulty; how much I counts against F is
   alpha/beta's job, so I is stretched to the same 1-3 range as F:
   - shapes with at least MIN_N BIRD questions: I = 1 + 2 * (fitted - min) / (max - min), with min and max
     taken over those shapes, rounded to 0.1;
   - shapes with fewer: keep the prior (the v1 hand-set value), since BIRD has too few examples to say.

Hand check (30 random questions, seed 11): 27 tagged correctly. The 3 errors were all missed shapes,
none spurious: "how many times more" (ratio), a ratio between two years (period comparison), and one BIRD
item whose question says "how many" while its SQL lists IDs. The ratio and period-comparison cues were
widened after the check.

Data: BIRD Mini-Dev (CC BY-SA 4.0), not committed. Fetch it with:
    mkdir -p downloads/bird_minidev && curl -sfL -o downloads/bird_minidev/mini_dev_sqlite_2025-07-04.json \
      https://huggingface.co/datasets/birdsql/bird_mini_dev/resolve/5b256b5a9c17478f06ed6912612e9a14d17065c8/archive/bird_mini_dev_2025-07-04/data/mini_dev_sqlite-00000-of-00001.json
The archived 2025-07-04 release is used on purpose: it keeps the original difficulty labels (30/50/20%).
The current release relabels 460 of 500 questions as challenging.
Run:
    uv run --group calibration python -I calibration/bird_i.py [--sample 30]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

import numpy as np
import sqlglot
from sqlglot import exp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "downloads" / "bird_minidev" / "mini_dev_sqlite_2025-07-04.json"
OUT = ROOT / "calibration" / "bird_i_results.json"
SOURCE = {
    "dataset": "BIRD Mini-Dev (SQLite), archived 2025-07-04 release (original difficulty labels, 30/50/20%)",
    "url": "https://huggingface.co/datasets/birdsql/bird_mini_dev",
    "revision": "5b256b5a9c17478f06ed6912612e9a14d17065c8",
    "path": "archive/bird_mini_dev_2025-07-04/data/mini_dev_sqlite-00000-of-00001.json",
    "why_not_current": "the 2026-10 'Mini-Dev 1024' release re-annotated questions for an agentic benchmark and labels 460/500 as challenging, so its labels can't separate shapes",
    "license": "CC BY-SA 4.0",
}
SHAPES = ["lookup", "aggregation", "multi_join", "ranking", "time_trend", "ratio", "vs_aggregate", "anti_join"]
OPS = [s for s in SHAPES if s != "lookup"]
LEVEL = {"simple": 1, "moderate": 2, "challenging": 3}
MIN_N = 20
PRIOR_I = {"lookup": 1, "aggregation": 2, "multi_join": 3, "ranking": 2, "time_trend": 3, "ratio": 3, "vs_aggregate": 3, "anti_join": 3}

RATIO_WORDS = re.compile(r"\b(percent|percentage|ratio|rate|proportion|share|fraction|times)\b", re.I)
CHANGE_WORDS = re.compile(r"\b(change|changed|increase|increased|decrease|decreased|growth|grew|difference|compared?|trend|from \d{4} to \d{4})\b", re.I)
DATE_NAME = re.compile(r"date|year|month|time|season", re.I)
YEAR_LIT = re.compile(r"^(19|20)\d{2}")
RANK_FUNCS = {"RANK", "DENSE_RANK", "ROW_NUMBER", "PERCENT_RANK", "NTILE"}
DATE_FUNCS = {"STRFTIME", "DATE", "DATETIME", "JULIANDAY", "YEAR", "MONTH", "SUBSTR", "SUBSTRING"}
COMPARE = (exp.GT, exp.GTE, exp.LT, exp.LTE, exp.NEQ)


def _func_name(node: exp.Expression) -> str:
    if isinstance(node, exp.Anonymous):
        return str(node.this).upper()
    return (node.sql_name() if hasattr(node, "sql_name") else type(node).__name__).upper()


def _has_agg(node: exp.Expression) -> bool:
    return any(True for _ in node.find_all(exp.AggFunc))


def _scalar_subquery_aggs(side: exp.Expression) -> list[str]:
    """Aggregate function names in the projections of scalar subqueries inside one side of a comparison."""
    names = []
    for sq in side.find_all(exp.Subquery):
        sel = sq.this if isinstance(sq.this, exp.Select) else sq.find(exp.Select)
        if sel is None:
            continue
        for proj in sel.expressions:
            names += [_func_name(a) for a in proj.find_all(exp.AggFunc)]
    return names


def _in_comparison_subquery(sel: exp.Select) -> bool:
    """True if this SELECT is a scalar subquery used inside a comparison (e.g. x > (SELECT AVG(x) ...))."""
    node = sel.parent
    while node is not None and not isinstance(node, exp.Select):
        if isinstance(node, (exp.GT, exp.GTE, exp.LT, exp.LTE, exp.EQ, exp.NEQ)):
            return True
        node = node.parent
    return False


def _is_date_expr(node: exp.Expression) -> bool:
    for f in node.find_all(exp.Func):
        if _func_name(f) in DATE_FUNCS or isinstance(f, (exp.TimeToStr, exp.StrToTime, exp.Year, exp.Month)):
            return True
    return any(DATE_NAME.search(c.name or "") for c in node.find_all(exp.Column))


def tag_shapes(sql: str, question: str) -> tuple[set[str], dict]:
    tree = sqlglot.parse_one(sql, read="sqlite")
    ctes = {c.alias_or_name.lower() for c in tree.find_all(exp.CTE)}
    tables = {t.name.lower() for t in tree.find_all(exp.Table) if t.name and t.name.lower() not in ctes}
    shapes: set[str] = set()

    if len(tables) >= 3:
        shapes.add("multi_join")

    # aggregation: an aggregate in a SELECT that isn't a scalar subquery inside a comparison
    for sel in tree.find_all(exp.Select):
        if _in_comparison_subquery(sel):
            continue
        parts = list(sel.expressions) + [sel.args.get("having"), sel.args.get("order")]
        if any(p is not None and _has_agg(p) for p in parts):
            shapes.add("aggregation")
            break

    # ranking: ORDER BY + LIMIT, a rank window function, or = (SELECT MAX/MIN ...)
    for sel in tree.find_all(exp.Select):
        if sel.args.get("order") is not None and sel.args.get("limit") is not None:
            shapes.add("ranking")
    for w in tree.find_all(exp.Window):
        if _func_name(w.this) in RANK_FUNCS:
            shapes.add("ranking")
    for eq in tree.find_all(exp.EQ):
        if {"MAX", "MIN"} & set(_scalar_subquery_aggs(eq.expression) + _scalar_subquery_aggs(eq.this)):
            shapes.add("ranking")

    # vs_aggregate: >, <, >=, <=, <> against a scalar subquery with an aggregate
    for cmp in tree.find_all(*COMPARE):
        if _scalar_subquery_aggs(cmp.expression) or _scalar_subquery_aggs(cmp.this):
            shapes.add("vs_aggregate")

    # anti_join: NOT IN (subquery), NOT EXISTS, EXCEPT, LEFT JOIN ... IS NULL, HAVING COUNT(..) = 0
    for n in tree.find_all(exp.Not):
        inner = n.this
        if isinstance(inner, exp.Exists) or (isinstance(inner, exp.In) and inner.args.get("query") is not None):
            shapes.add("anti_join")
    if any(True for _ in tree.find_all(exp.Except)):
        shapes.add("anti_join")
    left_join = any((j.side or "").upper() == "LEFT" for j in tree.find_all(exp.Join))
    if left_join and any(isinstance(i.expression, exp.Null) for i in tree.find_all(exp.Is)):
        shapes.add("anti_join")
    for sel in tree.find_all(exp.Select):
        h = sel.args.get("having")
        if h is not None:
            for eq in h.find_all(exp.EQ):
                if isinstance(eq.this, exp.Count) and isinstance(eq.expression, exp.Literal) and eq.expression.this == "0":
                    shapes.add("anti_join")

    # ratio: a division in the SQL and ratio wording in the question (separates shares from averages)
    if any(True for _ in tree.find_all(exp.Div)) and RATIO_WORDS.search(question):
        shapes.add("ratio")

    # time_trend: grouping by a date expression, or comparing periods (2+ year literals inside
    # aggregated CASE/IIF conditions) with change wording in the question
    for g in tree.find_all(exp.Group):
        if any(_is_date_expr(e) for e in g.expressions):
            shapes.add("time_trend")
    years = set()
    for agg in tree.find_all(exp.AggFunc):
        for cond in list(agg.find_all(exp.If)) + list(agg.find_all(exp.Case)):
            years |= {lit.this[:4] for lit in cond.find_all(exp.Literal) if lit.is_string and YEAR_LIT.match(lit.this)}
            years |= {lit.this for lit in cond.find_all(exp.Literal) if not lit.is_string and YEAR_LIT.match(lit.this) and len(lit.this) == 4}
    if len(years) >= 2 and (CHANGE_WORDS.search(question) or RATIO_WORDS.search(question)):
        shapes.add("time_trend")

    if not shapes - {"multi_join"}:
        shapes.add("lookup")
    return shapes, {"tables": sorted(tables)}


def fit(rows: list[dict], idx: np.ndarray | None = None) -> np.ndarray:
    """OLS of difficulty on [1, has_op...]. Returns per-shape predicted difficulty, in SHAPES order."""
    sub = rows if idx is None else [rows[i] for i in idx]
    X = np.array([[1.0] + [1.0 if s in r["shapes"] else 0.0 for s in OPS] for r in sub])
    y = np.array([r["level"] for r in sub], dtype=float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return np.array([b[0]] + [b[0] + b[1 + i] for i in range(len(OPS))])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--sample", type=int, default=0, help="print N random tagged questions for a hand check")
    ap.add_argument("--boot", type=int, default=2000)
    args = ap.parse_args()

    raw = args.data.read_bytes()
    rows, failed = [], []
    text = raw.decode()
    items = json.loads(text) if text.lstrip().startswith("[") else [json.loads(l) for l in text.splitlines() if l.strip()]
    for q in items:
        try:
            shapes, info = tag_shapes(q["SQL"], q["question"])
        except Exception as e:  # unparseable SQL is reported, not guessed
            failed.append({"id": q["question_id"], "error": str(e)[:120]})
            continue
        rows.append({"id": q["question_id"], "db": q["db_id"], "question": q["question"], "sql": q["SQL"],
                     "difficulty": q["difficulty"], "level": LEVEL[q["difficulty"]], "shapes": sorted(shapes), **info})

    point = fit(rows)
    X = np.array([[1.0] + [1.0 if s in r["shapes"] else 0.0 for s in OPS] for r in rows])
    y = np.array([r["level"] for r in rows], dtype=float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - float(np.sum((y - X @ b) ** 2) / np.sum((y - y.mean()) ** 2))
    rng = np.random.default_rng(7)
    boots = np.array([fit(rows, rng.integers(0, len(rows), len(rows))) for _ in range(args.boot)])
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)

    per_shape = {}
    for i, s in enumerate(SHAPES):
        with_s = [r["level"] for r in rows if s in r["shapes"]]
        per_shape[s] = {
            "n": len(with_s),
            "share_of_questions": round(len(with_s) / len(rows), 3),
            "mean_difficulty_when_present": round(float(np.mean(with_s)), 3) if with_s else None,
            "fitted_difficulty": round(float(point[i]), 3),
            "ci95": [round(float(lo[i]), 3), round(float(hi[i]), 3)],
        }
    well = {s: v["fitted_difficulty"] for s, v in per_shape.items() if v["n"] >= MIN_N}
    fmin, fmax = min(well.values()), max(well.values())
    for s, v in per_shape.items():
        if s in well:
            v["proposed_I"] = round(1 + 2 * (well[s] - fmin) / (fmax - fmin), 1)
            v["I_rule"] = f"stretched to 1-3 over shapes with n >= {MIN_N}"
        else:
            v["proposed_I"] = PRIOR_I[s]
            v["I_rule"] = f"prior kept (n < {MIN_N})"
    result = {
        "source": {**SOURCE, "sha256": hashlib.sha256(raw).hexdigest()},
        "questions": len(rows),
        "unparsed": failed,
        "difficulty_split": dict(Counter(r["difficulty"] for r in rows)),
        "shapes_per_question": dict(sorted(Counter(len(r["shapes"]) for r in rows).items())),
        "method": "OLS difficulty(1-3) ~ 1 + has_shape (lookup = baseline); fitted_difficulty = b0 (+ b_shape); 95% bootstrap CI",
        "r2": round(r2, 3),
        "per_shape": per_shape,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")

    print(f"{len(rows)} questions tagged, {len(failed)} unparsed. Difficulty: {result['difficulty_split']}. R^2 = {r2:.3f}")
    print(f"{'shape':<13} {'n':>4} {'share':>6} {'mean':>6} {'fitted':>7}  {'95% CI':<16} {'I':>4}  rule")
    for s, v in per_shape.items():
        print(f"{s:<13} {v['n']:>4} {v['share_of_questions']:>6} {v['mean_difficulty_when_present']!s:>6} "
              f"{v['fitted_difficulty']:>7}  {str(v['ci95']):<16} {v['proposed_I']:>4}  {v['I_rule']}")
    print(f"wrote {OUT.relative_to(ROOT)}")

    if args.sample:
        random.seed(11)
        for r in random.sample(rows, args.sample):
            print(f"\n#{r['id']} [{r['difficulty']}] {r['question']}\n  SQL: {r['sql']}\n  -> {r['shapes']}")


if __name__ == "__main__":
    main()
