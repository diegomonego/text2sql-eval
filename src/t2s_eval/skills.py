"""The three skills and the model each one is pinned to.

config/eval.toml is the source of truth for models. The `model:` line in each SKILL.md is synced
from it, because a skill's own model line decides which model runs, even over `claude --model`
(checked by running a probe skill both ways).
"""

from __future__ import annotations

import re
from pathlib import Path

from .config import Config

SKILL_FOR_COMPONENT = {
    "generator": "generate-questions",
    "correctness_judge": "judge-correctness",
    "coverage_judge": "judge-coverage",
}
LOG_FOR_COMPONENT = {
    "generator": "generator.json",
    "correctness_judge": "correctness.json",
    "coverage_judge": "coverage.json",
}

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_MODEL_LINE = re.compile(r"^model:[ \t]*(.*?)[ \t]*$", re.M)


def skill_path(root: Path, component: str) -> Path:
    return root / ".claude" / "skills" / SKILL_FOR_COMPONENT[component] / "SKILL.md"


def read_model(path: Path) -> str | None:
    m = _FRONTMATTER.match(path.read_text())
    if not m:
        return None
    line = _MODEL_LINE.search(m.group(1))
    return line.group(1) if line else None


def write_model(path: Path, model: str) -> bool:
    """Set the frontmatter's model line. Returns True when the file changed."""
    text = path.read_text()
    m = _FRONTMATTER.match(text)
    if not m:
        raise ValueError(f"{path}: no frontmatter")
    fm = m.group(1)
    if _MODEL_LINE.search(fm):
        new_fm = _MODEL_LINE.sub(lambda _: f"model: {model}", fm, count=1)
    else:
        new_fm = f"{fm}\nmodel: {model}"
    if new_fm == fm:
        return False
    path.write_text(text[: m.start(1)] + new_fm + text[m.end(1):])
    return True


def sync_skills(cfg: Config, check: bool = False) -> tuple[bool, list[str]]:
    """Copy each component's configured model into its skill (or, with check=True, only report drift).

    Returns (all skills already matched the config, one line per skill).
    """
    in_sync, lines = True, []
    for component, skill in SKILL_FOR_COMPONENT.items():
        path = skill_path(cfg.root, component)
        want, have = cfg.models[component], read_model(path)
        if have == want:
            lines.append(f"{skill}: {want}")
            continue
        in_sync = False
        if check:
            lines.append(f"{skill}: skill says {have}, config says {want} (run `make skills`)")
        else:
            write_model(path, want)
            lines.append(f"{skill}: {have} -> {want} (updated from config)")
    return in_sync, lines
