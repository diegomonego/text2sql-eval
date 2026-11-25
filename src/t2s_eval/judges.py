"""Judge steps run by the judge skills: prepare (before the LLM writes) and finalize (after).

The LLM writes only links, verdicts and rationales. Code checks the links, applies the credit
rules, computes every score and writes the JSON and Markdown reports.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .anchor import render_anchor_md
from .config import Config
from .db import connect
from .generator import _anchor, _docs_md, _write_json
from .legend import load_legend, render_legend_md
from .links import Analysis, Link, LinkChecker, label_check, link_record
from .meta import build_meta, list_docs, sha256_file
from .questions import judge_view, load_questions
from .render import render_correctness_md, render_coverage_md
from .schema_card import NOTE_CODED, NOTE_CONSTANT, build_schema_card, render_schema_card_md

VERDICTS = ("OFF_TOPIC", "MISSING_DATA", "AMBIGUOUS", "ANSWERABLE")
CORRECTNESS_FORMULA = "(ANSWERABLE + 0.5 x AMBIGUOUS) / N"
COVERAGE_FORMULA = "(table % + column % + shape %) / 3"


class Reading(BaseModel):
    model_config = ConfigDict(extra="ignore")
    description: str = ""
    links: list[Link] = Field(default_factory=list)


class CorrectnessItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    verdict: Literal["OFF_TOPIC", "MISSING_DATA", "AMBIGUOUS", "ANSWERABLE"]
    rationale: str = ""
    links: list[Link] = Field(default_factory=list)
    readings: list[Reading] = Field(default_factory=list)


class CoverageItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    links: list[Link] = Field(default_factory=list)
    note: str | None = None


def _work(out: Path, judge: str) -> Path:
    return out / "work" / judge


def prepare(cfg: Config, judge: str, questions_path: Path, out: Path, no_docs: bool, anchor_setting: str | None) -> str:
    questions, warnings = load_questions(questions_path)
    work = _work(out, judge)
    work.mkdir(parents=True, exist_ok=True)
    raw_path = work / "raw.json"
    if raw_path.exists():
        raw_path.unlink()
    db = connect(cfg.db_url, cfg.root)
    legend = load_legend(cfg.shapes_path)
    card = build_schema_card(db, cfg.max_listed_values)
    anchor = _anchor(cfg, anchor_setting, db)
    docs = list_docs(cfg, no_docs)
    _write_json(work / "settings.json", {"questions": str(questions_path), "no_docs": no_docs, "anchor": anchor})
    _write_json(work / "schema_card.json", card)
    (work / "schema_card.md").write_text(render_schema_card_md(card, docs_supplied=bool(docs)))
    _write_json(work / "questions_for_judge.json", {"questions": judge_view(questions)})
    rel = lambda p: str(p.relative_to(cfg.root)) if p.is_relative_to(cfg.root) else str(p)
    finalize_cmd = f"uv run t2s judge-finalize --judge {judge} --questions {rel(questions_path)} --out {rel(out)}"
    brief = f"""# {judge.capitalize()} judge brief

{len(questions)} questions to judge.

## Files to read
- `{rel(work / 'questions_for_judge.json')}`: the questions (ids and text only).
- `{rel(work / 'schema_card.md')}`: tables, columns, value ranges, listed values, joins.
- Docs: {_docs_md(cfg, docs)}

## Time anchor
{render_anchor_md(anchor)}

## Shape legend (use these ids in shape links)
{render_legend_md(legend)}

## Output
Write your judgments to `{rel(raw_path)}`, then run:
`{finalize_cmd}`
"""
    (work / "brief.md").write_text(brief)
    db.close()
    msg = f"Prepared the {judge} judge for {len(questions)} questions. Read {rel(work / 'brief.md')} first."
    if warnings:
        msg += "\nQuestion file warnings:\n" + "\n".join(f"- {w}" for w in warnings)
    return msg


def _id_issues(questions: list[dict[str, Any]], result_ids: list[str]) -> list[str]:
    issues = []
    expected = [q["id"] for q in questions]
    dup = sorted({i for i in result_ids if result_ids.count(i) > 1})
    if dup:
        issues.append(f"duplicate results for: {', '.join(dup)}")
    missing = [i for i in expected if i not in result_ids]
    if missing:
        issues.append(f"no result for: {', '.join(missing)}")
    extra = [i for i in result_ids if i not in expected]
    if extra:
        issues.append(f"results for unknown ids: {', '.join(extra)}")
    return issues


def _parse(raw_path: Path, model: type[BaseModel]) -> tuple[list[Any], list[str]]:
    if not raw_path.exists():
        return [], [f"{raw_path} does not exist"]
    try:
        data = json.loads(raw_path.read_text())
    except json.JSONDecodeError as e:
        return [], [f"{raw_path.name} is not valid JSON: {e}"]
    items, issues = [], []
    for i, item in enumerate(data.get("results", []) if isinstance(data, dict) else [], 1):
        try:
            items.append(model.model_validate(item))
        except ValidationError as e:
            err = e.errors()[0]
            issues.append(f"result #{i} ({item.get('id', '?') if isinstance(item, dict) else '?'}): {'.'.join(map(str, err['loc']))}: {err['msg']}")
    if not items and not issues:
        issues.append("expected an object with a non-empty 'results' list")
    return items, issues


# ---------------------------------------------------------------- correctness


def evaluate_correctness(questions: list[dict[str, Any]], items: list[CorrectnessItem], checker: LinkChecker) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    by_id = {it.id: it for it in items}
    results, issues = [], []
    for q in questions:
        it = by_id.get(q["id"])
        if it is None:
            continue
        a = checker.analyze(q["text"], it.links)
        ev: list[str] = []
        if not it.rationale.strip():
            ev.append("rationale is empty")
        for i, chk in a.failed:
            ev.append(f"link '{it.links[i].phrase}': {'; '.join(chk.problems)}")
        readings_out = []
        reading_ok = 0
        for r in it.readings:
            ra = checker.analyze(q["text"], r.links)
            if r.links and ra.all_links_ok and not ra.missing:
                reading_ok += 1
            readings_out.append({"description": r.description, "links": [link_record(l, c) for l, c in zip(r.links, ra.link_checks)]})
        if it.verdict == "ANSWERABLE":
            if not any(l.kind != "missing" for l in it.links):
                ev.append("ANSWERABLE needs links for the question's concepts")
            if a.missing:
                ev.append("ANSWERABLE but a concept is marked missing")
            if a.ambiguous:
                ev.append("ANSWERABLE but a link has alternatives (that is AMBIGUOUS)")
            if not a.connected:
                ev.append(f"ANSWERABLE but the linked tables don't connect ({', '.join(a.path_tables)})")
        elif it.verdict == "AMBIGUOUS":
            if reading_ok < 2 and not a.ambiguous:
                ev.append("AMBIGUOUS needs at least 2 readings with valid links, or a link with alternatives")
        elif it.verdict == "MISSING_DATA":
            if not a.missing:
                ev.append("MISSING_DATA needs a 'missing' link naming the concept")
        results.append(
            {
                "id": q["id"],
                "text": q["text"],
                "verdict": it.verdict,
                "rationale": it.rationale.strip(),
                "links": [link_record(l, c) for l, c in zip(it.links, a.link_checks)],
                "readings": readings_out,
                "missing": a.missing,
                "derived": {"tables": sorted(a.tables), "columns": sorted(a.columns), "shapes": sorted(a.shapes), "join_path": a.path_tables},
                "evidence_ok": not ev,
                "evidence_issues": ev,
                "label_check": label_check(q.get("labels"), a),
            }
        )
        issues += [f"{q['id']}: {e}" for e in ev]
    counts = {v: sum(1 for r in results if r["verdict"] == v) for v in VERDICTS}
    n = len(questions)
    score = (counts["ANSWERABLE"] + 0.5 * counts["AMBIGUOUS"]) / n if n else 0.0
    summary = {
        "n": n,
        "counts": counts,
        "score": round(score, 4),
        "formula": CORRECTNESS_FORMULA,
        "calculation": f"({counts['ANSWERABLE']} + 0.5 x {counts['AMBIGUOUS']}) / {n} = {score:.4f}",
        "verdicts_with_evidence_issues": sum(1 for r in results if not r["evidence_ok"]),
    }
    return results, summary, issues


# ---------------------------------------------------------------- coverage


def evaluate_coverage(
    questions: list[dict[str, Any]],
    items: list[CoverageItem],
    checker: LinkChecker,
    card: dict[str, Any],
    shape_ids: list[str],
    docs_supplied: bool,
) -> tuple[dict[str, Any], list[str]]:
    by_id = {it.id: it for it in items}
    per_q, issues = [], []
    credited: dict[str, dict[str, set[str]]] = {}
    for q in questions:
        it = by_id.get(q["id"])
        if it is None:
            continue
        a: Analysis = checker.analyze(q["text"], it.links)
        not_credited = []
        for i, chk in a.failed:
            not_credited.append({"phrase": it.links[i].phrase, "reason": "; ".join(chk.problems)})
            issues.append(f"{q['id']}: link '{it.links[i].phrase}': {'; '.join(chk.problems)}")
        for amb in a.ambiguous:
            not_credited.append({"phrase": amb["phrase"], "reason": "ambiguous: " + " | ".join(", ".join(r) for r in amb["readings"])})
        supported = not a.missing and a.connected
        if supported:
            got = {"tables": set(a.tables), "columns": set(a.columns), "shapes": set(a.shapes)}
        else:
            why = (
                f"concept not in the database: {', '.join(m['concept'] or m['phrase'] for m in a.missing)}"
                if a.missing else f"linked tables don't connect ({', '.join(a.path_tables)})"
            )
            for dim, vals in (("tables", a.tables), ("columns", a.columns), ("shapes", a.shapes)):
                for v in sorted(vals):
                    not_credited.append({"item": f"{dim}:{v}", "reason": f"question earns no credit: {why}"})
            got = {"tables": set(), "columns": set(), "shapes": set()}
        credited[q["id"]] = got
        per_q.append(
            {
                "id": q["id"],
                "text": q["text"],
                "supported": supported,
                "credited": {k: sorted(v) for k, v in got.items()},
                "not_credited": not_credited,
                "links": [link_record(l, c) for l, c in zip(it.links, a.link_checks)],
                "join_path": a.path_tables,
                "note": it.note,
                "label_check": label_check(q.get("labels"), a),
            }
        )
    eligible = {
        "tables": [t["name"] for t in card["tables"]],
        "columns": [f"{t['name']}.{c['name']}" for t in card["tables"] for c in t["columns"]],
        "shapes": list(shape_ids),
    }
    col_notes = {f"{t['name']}.{c['name']}": c["notes"] for t in card["tables"] for c in t["columns"]}
    covered: dict[str, dict[str, list[str]]] = {d: defaultdict(list) for d in eligible}
    for qid, got in credited.items():
        for d in eligible:
            for item in sorted(got[d]):
                covered[d][item].append(qid)
    dims = {}
    for d, items_ in eligible.items():
        unc = {}
        for item in items_:
            if item in covered[d]:
                continue
            reason = "not asked"
            if d == "columns":
                notes = col_notes.get(item, [])
                if NOTE_CONSTANT in notes:
                    reason = "not asked (constant in this data)"
                elif NOTE_CODED in notes and not docs_supplied:
                    reason = "not coverable without docs (coded values)"
            unc[item] = reason
        n_cov = sum(1 for i in items_ if i in covered[d])
        dims[d] = {
            "eligible": len(items_),
            "covered_count": n_cov,
            "pct": round(100 * n_cov / len(items_), 2) if items_ else 0.0,
            "covered": {i: covered[d][i] for i in items_ if i in covered[d]},
            "uncovered": unc,
        }
    # what each question alone covers
    for pq in per_q:
        uniq = []
        for d in eligible:
            for item in pq["credited"][d]:
                if covered[d][item] == [pq["id"]]:
                    uniq.append(f"{d}:{item}")
        pq["unique"] = uniq
    groups: dict[tuple, list[str]] = defaultdict(list)
    for pq in per_q:
        sig = tuple(tuple(pq["credited"][d]) for d in ("tables", "columns", "shapes"))
        if pq["supported"] and any(sig):
            groups[sig].append(pq["id"])
    dup_pairs = [[g[i], g[j]] for g in groups.values() for i in range(len(g)) for j in range(i + 1, len(g))]
    nothing_unique = [pq["id"] for pq in per_q if pq["supported"] and not pq["unique"]]
    no_credit = [pq["id"] for pq in per_q if not pq["supported"]]
    n = len(questions)
    score = sum(dims[d]["pct"] for d in dims) / 3
    supported_q = [pq for pq in per_q if pq["supported"]]
    avg_cols = sum(len(pq["credited"]["columns"]) for pq in supported_q) / len(supported_q) if supported_q else 0.0
    ceiling = min(len(eligible["columns"]), math.floor(avg_cols * n))
    n_amb = sum(1 for pq in per_q for nc in pq["not_credited"] if nc.get("reason", "").startswith("ambiguous"))
    budget_note = (
        f"N = {n}. There are {len(eligible['tables'])} tables, {len(eligible['columns'])} columns and "
        f"{len(eligible['shapes'])} shapes. A few questions that each combine several tables and shapes can cover "
        f"all tables and shapes; columns can't be covered that way. Credited questions here link "
        f"{avg_cols:.1f} columns on average, so even with no repetition at most about {ceiling} of "
        f"{len(eligible['columns'])} columns ({100 * ceiling / len(eligible['columns']):.0f}%) could be covered at this N; "
        f"{dims['columns']['covered_count']} were. Read column coverage relative to N. "
        f"{len(no_credit)} question(s) earned no credit (a concept not in the database, or tables that don't connect) "
        f"and {n_amb} ambiguous phrase(s) earned nothing."
    )
    report = {
        "per_question": per_q,
        "dimensions": dims,
        "repetition": {"duplicate_pairs": dup_pairs, "nothing_unique": nothing_unique, "no_credit": no_credit},
        "summary": {
            "n": n,
            "tables_pct": dims["tables"]["pct"],
            "columns_pct": dims["columns"]["pct"],
            "shapes_pct": dims["shapes"]["pct"],
            "score": round(score, 2),
            "formula": COVERAGE_FORMULA,
            "calculation": f"({dims['tables']['pct']} + {dims['columns']['pct']} + {dims['shapes']['pct']}) / 3 = {score:.2f}",
            "duplicate_pairs": len(dup_pairs),
            "questions_covering_nothing_unique": len(nothing_unique),
            "questions_without_credit": len(no_credit),
        },
        "budget_note": budget_note,
    }
    return report, issues


# ---------------------------------------------------------------- finalize


def finalize(cfg: Config, judge: str, questions_path: Path, out: Path, accept_issues: bool) -> tuple[int, str]:
    """0 = written; 2 = format problems (fix raw.json); 3 = evidence problems (fix, or rerun with --accept-issues)."""
    work = _work(out, judge)
    settings = json.loads((work / "settings.json").read_text())
    card = json.loads((work / "schema_card.json").read_text())
    questions, _ = load_questions(questions_path)
    model = CorrectnessItem if judge == "correctness" else CoverageItem
    items, fmt = _parse(work / "raw.json", model)
    fmt += _id_issues(questions, [it.id for it in items])
    if fmt:
        return 2, "FORMAT PROBLEMS in raw.json (fix and run again):\n" + "\n".join(f"- {x}" for x in fmt)
    db = connect(cfg.db_url, cfg.root)
    legend = load_legend(cfg.shapes_path)
    checker = LinkChecker(card, db, legend)
    docs = list_docs(cfg, settings["no_docs"])
    if judge == "correctness":
        results, summary, issues = evaluate_correctness(questions, items, checker)
        body: dict[str, Any] = {"results": results, "summary": summary}
    else:
        body, issues = evaluate_coverage(questions, items, checker, card, legend.ids, bool(docs))
        summary = body["summary"]
    if issues and not accept_issues:
        db.close()
        return 3, (
            "EVIDENCE PROBLEMS (fix raw.json and run again; if you cannot fix them, rerun with --accept-issues "
            "and they will be flagged in the report):\n" + "\n".join(f"- {x}" for x in issues)
        )
    meta = build_meta(
        f"{judge}_judge",
        cfg,
        db.fingerprint(),
        docs,
        settings["anchor"],
        {"questions_file": str(questions_path.relative_to(cfg.root)) if questions_path.resolve().is_relative_to(cfg.root) else str(questions_path),
         "questions_sha256": sha256_file(questions_path), "n": len(questions), "issues_accepted": len(issues)},
    )
    report = {"meta": meta, **body}
    _write_json(out / f"{judge}.json", report)
    md = render_correctness_md(report) if judge == "correctness" else render_coverage_md(report)
    (out / f"{judge}.md").write_text(md)
    db.close()
    return 0, f"Wrote {out / (judge + '.json')} and {judge}.md. Score: {summary['score']} ({summary['calculation']})." + (
        f" {len(issues)} evidence issue(s) flagged." if issues else ""
    )
