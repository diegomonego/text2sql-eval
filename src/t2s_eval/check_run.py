"""Consistency check across the files of one run folder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .meta import sha256_file


def _get(d: dict[str, Any], path: str) -> Any:
    for key in path.split("."):
        if not isinstance(d, dict):
            return None
        d = d.get(key)
    return d


# Must agree across the files of a run. Models may differ per component, so they're checked
# separately against each run's log.
FIELDS = {
    "database file": "database.file_sha256",
    "database data": "database.data_sha256",
    "docs": "docs",
    "time anchor date": "config.time_anchor.date",
    "shape legend": "config.shapes_toml_sha256",
    "config": "config.eval_toml_sha256",
}


def _model_from_log(log: Path) -> str | None:
    """The model that did the work in a `claude -p --output-format json` log (largest cost)."""
    usage = json.loads(log.read_text()).get("modelUsage") or {}
    if not usage:
        return None
    return max(usage, key=lambda k: usage[k].get("costUSD", 0))


def _claimed_vs_verified(qfile: Path, coverage_file: Path) -> list[str]:
    """Coverage the generator claims (its labels) against coverage the judge verified from its own links.
    Informational: a gap means the two readings of the questions differ, not that a file is inconsistent."""
    questions = json.loads(qfile.read_text()).get("questions", [])
    if not all("labels" in q for q in questions):
        return ["note: questions.json has no generator labels (edited or hand-written), so claimed coverage isn't known"]
    dims = json.loads(coverage_file.read_text())["dimensions"]
    out = []
    for d in ("tables", "columns", "shapes"):
        claimed = set().union(*[set(q["labels"].get(d, [])) for q in questions]) if questions else set()
        verified = set(dims[d]["covered"])
        extra = sorted(claimed - verified)
        out.append(
            f"claimed vs verified {d}: generator {len(claimed)}, coverage judge {len(verified)}"
            + (f"; claimed but not verified: {', '.join(extra)}" if extra else "")
        )
    return out


def check_run(folder: Path) -> tuple[int, str]:
    metas: dict[str, dict[str, Any]] = {}
    for name, rel in (("generator", "generation/run.json"), ("correctness", "correctness.json"), ("coverage", "coverage.json")):
        p = folder / rel
        if p.exists():
            data = json.loads(p.read_text())
            metas[name] = data if name == "generator" else data["meta"]
    if not metas:
        return 1, f"no outputs found in {folder}"
    lines, problems = [f"Run folder {folder}: found {', '.join(metas)}"], 0
    for label, path in FIELDS.items():
        values = {name: json.dumps(_get(m, path), sort_keys=True) for name, m in metas.items()}
        if len(set(values.values())) > 1:
            problems += 1
            lines.append(f"MISMATCH {label}: " + "; ".join(f"{k}={v[:60]}" for k, v in values.items()))
    from .skills import LOG_FOR_COMPONENT

    for name, m in metas.items():
        component, recorded = m["run"]["component"], m["run"].get("model")
        log = folder / "logs" / LOG_FOR_COMPONENT.get(component, "")
        actual = _model_from_log(log) if log.is_file() else None
        if actual is None:
            lines.append(f"note {name}: no run log, so the model that actually ran can't be checked (metadata says {recorded})")
        elif actual != recorded:
            problems += 1
            lines.append(f"MISMATCH {name}: metadata says {recorded}, but the run log shows {actual} did the work")
        else:
            lines.append(f"{name}: ran on {actual}")
    qfile = folder / "questions.json"
    if qfile.exists() and "coverage" in metas:
        lines += _claimed_vs_verified(qfile, folder / "coverage.json")
    if qfile.exists():
        current = sha256_file(qfile)
        for name in ("correctness", "coverage"):
            if name in metas and metas[name]["input"].get("questions_sha256") != current:
                problems += 1
                lines.append(f"MISMATCH {name}: judged a different version of questions.json than the current one")
    lines.append("OK: all files agree" if not problems else f"{problems} mismatch(es)")
    return (0 if not problems else 1), "\n".join(lines)
