"""Run metadata: records exactly what produced each output file."""

from __future__ import annotations

import datetime as dt
import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .config import Config


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_docs(cfg: Config, no_docs: bool) -> list[Path]:
    """All Markdown/text documents under the docs directory, unless docs are switched off."""
    if no_docs or not cfg.docs_dir.is_dir():
        return []
    return sorted(p for p in cfg.docs_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"})


def _git(root: Path) -> dict[str, Any]:
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=True).stdout.strip())
        return {"commit": commit, "uncommitted_changes": dirty}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": "not a git repository", "uncommitted_changes": None}


def _claude_version() -> str:
    for exe in [shutil.which("claude"), str(Path.home() / ".local" / "bin" / "claude")]:
        if exe and Path(exe).exists():
            try:
                return subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20).stdout.strip() or "unknown"
            except (OSError, subprocess.TimeoutExpired):
                continue
    return "unknown"


def _skill_sha(root: Path, component: str) -> str | None:
    from .skills import SKILL_FOR_COMPONENT, skill_path

    if component not in SKILL_FOR_COMPONENT:
        return None
    path = skill_path(root, component)
    return sha256_file(path) if path.is_file() else None


def build_meta(
    component: str,
    cfg: Config,
    db_fingerprint: dict[str, Any],
    docs: list[Path],
    anchor: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run": {
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
            "component": component,
            "git": _git(cfg.root),
            "claude_code_version": _claude_version(),
            "model": cfg.models.get(component, "unknown"),
            "skill_sha256": _skill_sha(cfg.root, component),
        },
        "database": db_fingerprint,
        "docs": [{"path": str(p.relative_to(cfg.root)), "sha256": sha256_file(p)} for p in docs] or "none",
        "config": {
            "shapes_toml_sha256": sha256_file(cfg.shapes_path) if cfg.shapes_path else None,
            "eval_toml_sha256": sha256_file(cfg.root / "config" / "eval.toml"),
            "time_anchor": {"setting": anchor.get("setting"), "mode": anchor["mode"], "date": anchor["date"]},
        },
        "input": inputs,
    }
