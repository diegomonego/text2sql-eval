"""Generator steps run by the generate-questions skill: prepare (before the LLM writes) and select (after)."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .anchor import render_anchor_md, resolve_anchor
from .config import Config, Preset
from .db import connect
from .diagnostics import selection_diagnostics
from .legend import load_legend, render_legend_md
from .links import Link, LinkChecker, link_record
from .meta import build_meta, list_docs, resolve_inputs, saved_inputs, show_path
from .schema_card import build_schema_card, render_schema_card_md
from .selection import GainSettings, NotEnoughCandidates, Scored, dedupe, greedy_select
from .targets import build_targets, pool_sizes

SQL_TERMS = re.compile(r"\b(SELECT|GROUP BY|ORDER BY|JOIN|WHERE|HAVING|LEFT JOIN|INNER JOIN)\b")


class Candidate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    target: str = ""
    question: str
    links: list[Link] = Field(default_factory=list)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def _anchor(cfg: Config, setting: str | None, db: Any) -> dict[str, Any]:
    setting = setting or cfg.anchor_mode
    anchor = resolve_anchor(setting, cfg.anchor_column, db)
    anchor["setting"] = setting
    return anchor


def _docs_md(cfg: Config, docs: list[Path]) -> str:
    if not docs:
        return "**No docs supplied.** Work from the schema card alone. Avoid columns noted as coded, and use explicit metric wording (e.g. \"total order value\", not \"revenue\")."
    return "Read every one of these documents in full:\n\n" + "\n".join(f"- `{show_path(p, cfg.root)}`" for p in docs)


def min_free_picks(preset: Preset, n: int) -> int:
    return math.ceil(preset.min_free_share * n - 1e-9) if preset.min_free_share else 0


def _preset_md(preset: Preset, n: int) -> str:
    """The brief's preset section: how to write candidates under this preset."""
    if preset.style == "natural":
        k = min_free_picks(preset, n)
        cap = preset.max_shapes
        lines = [
            f"**{preset.name}**: everyday questions.",
            "",
            "- **Write each question the way it would arrive in a ticket or a chat message** from a colleague: one ask, plainly worded.",
            "- **Don't stack extra filters or conditions just to reach more columns.** A natural question that reuses common columns beats a contrived one.",
        ]
        if cap:
            lines.append(
                f"- **At most {cap} shapes per question.** Code drops candidates with more. The derived `multi_join` counts: "
                f"a question that needs 3 or more tables already uses one of the {cap}."
            )
        if not preset.focus_tables:
            lines.append("- **Targets name a shape only.** Choose whatever tables make the question natural.")
        if k:
            lines.append(
                f"- **Free candidates carry extra weight:** at least {k} of the {n} picks must come from them. Make them the questions this business asks most often."
            )
        return "\n".join(lines)
    return "\n".join(
        [
            f"**{preset.name}**: spread questions across the schema.",
            "",
            "- **Use as many different columns as possible across all candidates.** Prefer columns earlier candidates haven't used, "
            "including less obvious ones (for example containers, shipping instructions, clerks, account balances, supply costs, "
            "available quantities, sizes, tax).",
            "- **Combine shapes only where a real analyst would ask it that way.**",
        ]
    )


def prepare(
    cfg: Config,
    n: int,
    out: Path,
    no_docs: bool,
    anchor_setting: str | None,
    preset_name: str | None = None,
    db_url: str | None = None,
    docs: str | None = None,
) -> str:
    if n < 1:
        raise ValueError("--n must be a positive integer")
    db_url, docs_dir = resolve_inputs(cfg, db_url, docs, no_docs)
    preset = cfg.get_preset(preset_name)
    pool_settings = cfg.pool_for(preset)
    gen = out / "generation"
    gen.mkdir(parents=True, exist_ok=True)
    for old in gen.glob("candidates*.json"):
        old.unlink()
    db = connect(db_url, cfg.root)
    legend = load_legend(cfg.shapes_path)
    card = build_schema_card(db, cfg.max_listed_values)
    anchor = _anchor(cfg, anchor_setting, db)
    docs = list_docs(cfg, no_docs, docs_dir)
    targets = build_targets(n, legend.ids, card, pool_settings, preset.focus_tables)
    targeted, free = pool_sizes(n, pool_settings)
    _write_json(
        gen / "settings.json",
        {"n": n, "db_url": db_url, "docs_dir": show_path(docs_dir, cfg.root), "no_docs": no_docs, "anchor": anchor,
         "preset": preset.to_dict()},
    )
    _write_json(gen / "schema_card.json", card)
    (gen / "schema_card.md").write_text(render_schema_card_md(card, docs_supplied=bool(docs)))
    _write_json(gen / "targets.json", targets)
    rel = lambda p: str(p.relative_to(cfg.root)) if p.is_relative_to(cfg.root) else str(p)
    target_rows = "\n".join(
        f"| `{t['id']}` | {t['kind']} | {t.get('shape', '-')} | {t.get('focus_table', '-')} |" for t in targets
    )
    brief = f"""# Generation brief

N = {n}. Pool: {targeted} targeted + {free} free = {len(targets)} candidates (one per target below).
Code will check every candidate, remove duplicates and select exactly {n}.

## Files to read
- `{rel(gen / 'schema_card.md')}`: tables, columns, value ranges, listed values, joins.
- Docs: {_docs_md(cfg, docs)}

## Preset
{_preset_md(preset, n)}

## Time anchor
{render_anchor_md(anchor)}

## Shape legend (use these ids in shape links)
{render_legend_md(legend)}

## Targets
| target | kind | shape | focus table |
|---|---|---|---|
{target_rows}

## Output
Write all candidates to `{rel(gen / 'candidates.json')}`, then run:
`uv run t2s gen-select --out {rel(out)}`
"""
    (gen / "brief.md").write_text(brief)
    db.close()
    return (
        f"Prepared generation for N={n} in {rel(out)} with the {preset.name} preset.\n"
        f"Read {rel(gen / 'brief.md')} first. Then write {len(targets)} candidates "
        f"(one per target) to {rel(gen / 'candidates.json')} and run: uv run t2s gen-select --out {rel(out)}"
    )


def _lint(question: str, column_names: set[str]) -> str | None:
    if not question.strip():
        return "empty question"
    m = SQL_TERMS.search(question)
    if m:
        return f"uses SQL term '{m.group(1)}'"
    for name in column_names:
        if "_" in name and re.search(rf"\b{re.escape(name)}\b", question, re.I):
            return f"mentions raw column name '{name}'"
    return None


def select(cfg: Config, out: Path) -> tuple[int, str]:
    """Check, dedupe and select. Returns (exit code, message). 0 = done, 4 = need more candidates."""
    gen = out / "generation"
    settings = json.loads((gen / "settings.json").read_text())
    n, no_docs, anchor = settings["n"], settings["no_docs"], settings["anchor"]
    preset = Preset(**settings["preset"]) if "preset" in settings else Preset("coverage")
    quota = min_free_picks(preset, n)
    card = json.loads((gen / "schema_card.json").read_text())
    targets = {t["id"]: t for t in json.loads((gen / "targets.json").read_text())}
    files = sorted(gen.glob("candidates*.json"), key=lambda p: (len(p.name), p.name))
    if not files:
        return 2, f"no candidates file found in {gen}"
    db_url, docs_dir = saved_inputs(cfg, settings)  # the same inputs gen-prepare used
    db = connect(db_url, cfg.root)
    legend = load_legend(cfg.shapes_path)
    checker = LinkChecker(card, db, legend)
    docs = list_docs(cfg, no_docs, docs_dir)
    coded = checker.coded_columns() if not docs else set()
    column_names = {c["name"] for t in card["tables"] for c in t["columns"]}

    pool: list[dict[str, Any]] = []
    valid: list[Scored] = []
    k = 0
    for f in files:
        try:
            raw = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            return 2, f"{f.name} is not valid JSON: {e}. Fix the file and run gen-select again."
        items = raw.get("candidates", []) if isinstance(raw, dict) else []
        for item in items:
            k += 1
            cid = f"c{k:03d}"
            rec: dict[str, Any] = {"id": cid, "file": f.name}
            try:
                cand = Candidate.model_validate(item)
            except ValidationError as e:
                rec.update(status="dropped", reason=f"invalid format: {e.errors()[0]['msg']}", raw=item)
                pool.append(rec)
                continue
            rec.update(target=cand.target, question=cand.question.strip())
            a = checker.analyze(cand.question, cand.links)
            rec["links"] = [link_record(l, c) for l, c in zip(cand.links, a.link_checks)]
            rec["derived"] = {"tables": sorted(a.tables), "columns": sorted(a.columns), "shapes": sorted(a.shapes), "join_path": a.path_tables}
            reason = _lint(cand.question, column_names)
            if not reason and a.failed:
                i, chk = a.failed[0]
                reason = f"link '{cand.links[i].phrase}': {chk.problems[0]}"
            if not reason and a.missing:
                reason = f"concept not in the database: {a.missing[0]['concept']}"
            if not reason and a.ambiguous:
                reason = f"ambiguous link: '{a.ambiguous[0]['phrase']}'"
            if not reason and not a.connected:
                reason = f"linked tables don't connect: {', '.join(a.path_tables)}"
            if not reason and not a.shapes:
                reason = "no shape linked"
            if not reason and not (a.columns or a.tables):
                reason = "no table or column linked"
            if not reason and coded & a.columns:
                reason = f"uses coded column without docs: {', '.join(sorted(coded & a.columns))}"
            if not reason and preset.max_shapes and len(a.shapes) > preset.max_shapes:
                reason = (
                    f"{len(a.shapes)} shapes ({', '.join(sorted(a.shapes))}); the {preset.name} preset allows at most "
                    f"{preset.max_shapes}, and the derived multi_join counts"
                )
            if reason:
                rec.update(status="dropped", reason=reason)
            else:
                rec["status"] = "valid"
                valid.append(Scored(cid, frozenset(a.tables), frozenset(a.columns), frozenset(a.shapes), {"target": cand.target}))
            pool.append(rec)

    unique, dups = dedupe(valid)
    for rec in pool:
        if rec["id"] in dups:
            rec.update(status="duplicate", duplicate_of=dups[rec["id"]])
    alpha = preset.alpha if preset.alpha is not None else legend.alpha
    beta = preset.beta if preset.beta is not None else legend.beta
    is_free = lambda c: targets.get(c.extra.get("target", ""), {}).get("kind") == "free"
    gs = GainSettings(
        weights=legend.weights_for(alpha, beta),
        repeat_penalty=legend.repeat_penalty,
        lambda_shape=cfg.lambda_shape,
        lambda_table=cfg.lambda_table,
        lambda_column=cfg.lambda_column,
        n_tables=card["eligible"]["tables"],
        n_columns=card["eligible"]["columns"],
    )
    _write_json(gen / "pool.json", {"candidates": pool})
    dropped = [r for r in pool if r["status"] == "dropped"]
    drop_lines = "\n".join(f"- {r['id']} ({r.get('target', '?')}): {r['reason']}" for r in dropped) or "- none"
    try:
        picks, log = greedy_select(unique, n, gs, quota, is_free if quota else None)
    except NotEnoughCandidates as e:
        covered_targets = {c.extra["target"] for c in unique}
        missing_targets = [t for tid, t in targets.items() if tid not in covered_targets]
        rounds_used = len(files) - 1
        tlines = ", ".join(f"{t['id']} ({t.get('shape', 'free')}/{t.get('focus_table', '-')})" for t in missing_targets[: 2 * n])
        if rounds_used >= cfg.pool.max_refill_rounds:
            db.close()
            return 5, f"FAILED: {e} after {rounds_used} extra rounds. Giving up.\nDropped:\n{drop_lines}"
        db.close()
        return 4, (
            f"NOT ENOUGH CANDIDATES: {e}. Write new candidates (same format) to "
            f"{gen.name}/candidates_round{rounds_used + 2}.json for these targets, avoiding the drop reasons below, "
            f"then run gen-select again.\nTargets without a valid candidate: {tlines}\nDropped:\n{drop_lines}"
        )

    by_id = {r["id"]: r for r in pool}
    pick_ids = [p.id for p in picks]
    for r in pool:
        if r["status"] == "valid":
            r["status"] = "selected" if r["id"] in pick_ids else "not selected"
    questions = []
    for i, p in enumerate(picks, 1):
        r = by_id[p.id]
        r["question_id"] = f"q{i:02d}"
        questions.append(
            {
                "id": f"q{i:02d}",
                "text": r["question"],
                "labels": {"tables": sorted(p.tables), "columns": sorted(p.columns), "shapes": sorted(p.shapes)},
            }
        )
    _write_json(out / "questions.json", {"questions": questions})
    _write_json(gen / "pool.json", {"candidates": pool})
    _write_json(
        gen / "pick_log.json",
        {
            "settings": {**gs.__dict__, "sum_weights": gs.sum_weights, "alpha": alpha, "beta": beta,
                         "preset": preset.name, "min_free_picks": quota, "max_shapes": preset.max_shapes},
            "rounds": log,
        },
    )
    diag = selection_diagnostics(unique, picks, gs, legend, alpha, beta, is_free, quota)
    _write_json(gen / "diagnostics.json", {"preset": preset.name, "n": n, **diag})
    counts = {s: sum(1 for r in pool if r["status"] == s) for s in ("selected", "not selected", "duplicate", "dropped")}
    meta = build_meta(
        "generator",
        cfg,
        db.fingerprint(),
        docs,
        anchor,
        {"n": n, "preset": preset.to_dict(), "pool_size": len(pool), "candidate_files": [f.name for f in files], **{f"candidates_{k.replace(' ', '_')}": v for k, v in counts.items()}},
    )
    _write_json(gen / "run.json", meta)
    db.close()
    covered = {"tables": set(), "columns": set(), "shapes": set()}
    for p in picks:
        covered["tables"] |= p.tables
        covered["columns"] |= p.columns
        covered["shapes"] |= p.shapes
    qlines = "\n".join(f"- {q['id']}: {q['text']}" for q in questions)
    gb = diag["greedy_vs_best"]
    return 0, (
        f"Selected {n} of {len(pool)} candidates ({counts['dropped']} dropped, {counts['duplicate']} duplicates), "
        f"{preset.name} preset, {diag['free_form']['picks']} from free-form slots. "
        f"Greedy reached {gb['greedy_over_best']:.1%} of the best subset ({gb['method'].split(',')[0]}). "
        f"Covers {len(covered['tables'])}/{gs.n_tables} tables, {len(covered['columns'])}/{gs.n_columns} columns, "
        f"{len(covered['shapes'])}/{len(legend.ids)} shapes.\nWrote {show_path(out / 'questions.json', cfg.root)}\n{qlines}\nDropped:\n{drop_lines}"
    )
