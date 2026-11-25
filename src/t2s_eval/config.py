"""Project configuration (config/eval.toml) and repository paths."""

from __future__ import annotations

import os
import tomllib
from dataclasses import asdict, dataclass, field, replace
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
CONFIG_ENV = "T2S_CONFIG"  # path to another eval.toml (e.g. for a different database), relative to the repo root


@dataclass(frozen=True)
class PoolSettings:
    min_targeted: int = 16
    targeted_per_n: int = 2
    free_per_n: int = 1
    max_refill_rounds: int = 2


STYLES = ("coverage", "natural")


@dataclass(frozen=True)
class Preset:
    """Named generator settings (config/eval.toml [presets.<name>]), chosen per run with --preset."""

    name: str
    style: str = "coverage"  # which preset section the generation brief gets
    free_per_n: int | None = None  # overrides [pool] free_per_n
    focus_tables: bool = True  # targeted slots name a focus table
    min_free_share: float = 0.0  # at least ceil(share * N) picks come from free-form slots
    max_shapes: int | None = None  # candidates with more shapes are dropped (derived multi_join counts)
    alpha: float | None = None  # override the shape legend's alpha/beta for selection
    beta: float | None = None

    def __post_init__(self) -> None:
        if self.style not in STYLES:
            raise ValueError(f"preset {self.name}: style must be one of {', '.join(STYLES)}, got {self.style!r}")
        if not 0 <= self.min_free_share <= 1:
            raise ValueError(f"preset {self.name}: min_free_share must be between 0 and 1")
        if self.max_shapes is not None and self.max_shapes < 1:
            raise ValueError(f"preset {self.name}: max_shapes must be at least 1")
        if (self.alpha is None) != (self.beta is None):
            raise ValueError(f"preset {self.name}: set both alpha and beta, or neither")
        if self.alpha is not None and abs(self.alpha + self.beta - 1) > 1e-9:
            raise ValueError(f"preset {self.name}: alpha and beta must sum to 1")
        if self.free_per_n is not None and self.free_per_n < 0:
            raise ValueError(f"preset {self.name}: free_per_n can't be negative")

    def to_dict(self) -> dict:
        return asdict(self)


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
    presets: dict[str, Preset] = field(default_factory=lambda: {"coverage": Preset("coverage")})
    default_preset: str = "coverage"
    config_path: Path | None = None  # the eval.toml actually loaded

    def resolve(self, path: str | Path) -> Path:
        p = Path(path)
        return p if p.is_absolute() else self.root / p

    def get_preset(self, name: str | None = None) -> Preset:
        name = name or self.default_preset
        if name not in self.presets:
            raise ValueError(f"unknown preset {name!r}; config/eval.toml defines: {', '.join(self.presets)}")
        return self.presets[name]

    def pool_for(self, preset: Preset) -> PoolSettings:
        return self.pool if preset.free_per_n is None else replace(self.pool, free_per_n=preset.free_per_n)


def config_file(root: Path) -> Path:
    """config/eval.toml, or the file named by the T2S_CONFIG environment variable."""
    override = os.environ.get(CONFIG_ENV)
    if not override:
        return root / "config" / "eval.toml"
    path = Path(override)
    path = path if path.is_absolute() else root / path
    if not path.is_file():
        raise FileNotFoundError(f"{CONFIG_ENV}={override} does not point to a file")
    return path


def load_config(root: Path | None = None) -> Config:
    root = root or find_root()
    path = config_file(root)
    data = tomllib.loads(path.read_text())
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
    preset_data = dict(data.get("presets", {}))
    default_preset = str(preset_data.pop("default", "coverage"))
    presets = {name: Preset(name=name, **values) for name, values in preset_data.items()} or {"coverage": Preset("coverage")}
    if default_preset not in presets:
        raise ValueError(f"[presets] default = {default_preset!r} is not defined in config/eval.toml")
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
        presets=presets,
        default_preset=default_preset,
        config_path=path,
    )
