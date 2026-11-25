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


def show_path(path: Path, root: Path) -> str:
    """A path relative to the repo root when it is inside it, otherwise absolute."""
    return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)


def resolve_inputs(cfg: Config, db_url: str | None, docs: str | None, no_docs: bool) -> tuple[str, Path]:
    """The database connection and docs folder for a run: the --db / --docs arguments when given,
    otherwise the config. Shared by the generator and both judges."""
    if docs and no_docs:
        raise ValueError("--docs and --no-docs can't be combined")
    docs_dir = cfg.resolve(docs) if docs else cfg.docs_dir
    if docs and not docs_dir.is_dir():
        raise ValueError(f"--docs {docs}: not a directory")
    return db_url or cfg.db_url, docs_dir


def saved_inputs(cfg: Config, settings: dict) -> tuple[str, Path]:
    """The inputs a prepare step recorded in settings.json (falls back to the config for older runs)."""
    db_url = settings.get("db_url") or cfg.db_url
    docs_dir = cfg.resolve(settings["docs_dir"]) if settings.get("docs_dir") else cfg.docs_dir
    return db_url, docs_dir


def list_docs(cfg: Config, no_docs: bool, docs_dir: Path | None = None) -> list[Path]:
    """All Markdown/text documents under the docs directory (the config's, or `docs_dir` when given),
    unless docs are switched off."""
    folder = docs_dir or cfg.docs_dir
    if no_docs or not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"})


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
        "docs": [{"path": show_path(p, cfg.root), "sha256": sha256_file(p)} for p in docs] or "none",
        "config": {
            "shapes_toml_sha256": sha256_file(cfg.shapes_path) if cfg.shapes_path else None,
            "eval_toml_sha256": sha256_file(cfg.config_path or cfg.root / "config" / "eval.toml"),
            "eval_toml": str(cfg.config_path.relative_to(cfg.root)) if cfg.config_path and cfg.config_path.is_relative_to(cfg.root) else str(cfg.config_path),
            "time_anchor": {"setting": anchor.get("setting"), "mode": anchor["mode"], "date": anchor["date"]},
        },
        "input": inputs,
    }
