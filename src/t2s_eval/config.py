"""Project configuration (config/eval.toml) and repository paths."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


def find_root(start: Path | None = None) -> Path:
    """Return the repository root: the nearest directory holding config/eval.toml."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "config" / "eval.toml").is_file():
            return candidate
    package_root = Path(__file__).resolve().parents[2]
    if (package_root / "config" / "eval.toml").is_file():
        return package_root
    raise FileNotFoundError("config/eval.toml not found in this directory or any parent")


COMPONENTS = ("generator", "correctness_judge", "coverage_judge")


@dataclass(frozen=True)
class PoolSettings:
    min_targeted: int = 16
    targeted_per_n: int = 2
    free_per_n: int = 1
    max_refill_rounds: int = 2


@dataclass(frozen=True)
class Config:
    root: Path
    db_url: str
    docs_dir: Path
    anchor_mode: str
    anchor_column: str | None
    lambda_shape: float
    lambda_table: float
    lambda_column: float
    pool: PoolSettings = field(default_factory=PoolSettings)
    max_listed_values: int = 25
    models: dict[str, str] = field(default_factory=dict)  # component -> model id
    shapes_path: Path | None = None
    spec_url: str | None = None
    spec_sha256: str | None = None

    def resolve(self, path: str | Path) -> Path:
        p = Path(path)
        return p if p.is_absolute() else self.root / p


def load_config(root: Path | None = None) -> Config:
    root = root or find_root()
    data = tomllib.loads((root / "config" / "eval.toml").read_text())
    sel = data.get("selection", {})
    pool = data.get("pool", {})
    anchor = data.get("time_anchor", {})
    spec = data.get("spec", {})
    total = sel.get("lambda_shape", 0.5) + sel.get("lambda_table", 0.25) + sel.get("lambda_column", 0.25)
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"selection lambdas must sum to 1, got {total}")
    model = data.get("model", {})
    models = {c: model.get(c, model.get("id")) for c in COMPONENTS}  # `id` = one model for all
    missing = [c for c, v in models.items() if not v]
    if missing:
        raise ValueError(f"[model] in config/eval.toml has no model for: {', '.join(missing)}")
    return Config(
        root=root,
        db_url=data["database"]["url"],
        docs_dir=root / data.get("docs", {}).get("dir", "semantic_docs"),
        anchor_mode=str(anchor.get("mode", "off")),
        anchor_column=anchor.get("column") or None,
        lambda_shape=sel.get("lambda_shape", 0.5),
        lambda_table=sel.get("lambda_table", 0.25),
        lambda_column=sel.get("lambda_column", 0.25),
        pool=PoolSettings(
            min_targeted=pool.get("min_targeted", 16),
            targeted_per_n=pool.get("targeted_per_n", 2),
            free_per_n=pool.get("free_per_n", 1),
            max_refill_rounds=pool.get("max_refill_rounds", 2),
        ),
        max_listed_values=data.get("profile", {}).get("max_listed_values", 25),
        models=models,
        shapes_path=root / "config" / "shapes.toml",
        spec_url=spec.get("url"),
        spec_sha256=spec.get("sha256"),
    )
