"""Shape legend (config/shapes.toml): definitions, F/I scores and computed weights."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Shape:
    id: str
    name: str
    description: str
    example: str
    triggers: tuple[str, ...]
    F: float
    I: float
    reason: str
    derived: bool
    weight: float


@dataclass(frozen=True)
class Legend:
    alpha: float
    beta: float
    repeat_penalty: float
    shapes: tuple[Shape, ...]

    @property
    def ids(self) -> list[str]:
        return [s.id for s in self.shapes]

    @property
    def weights(self) -> dict[str, float]:
        return {s.id: s.weight for s in self.shapes}

    def weights_for(self, alpha: float | None = None, beta: float | None = None) -> dict[str, float]:
        """Weights with alpha/beta overridden (a preset's setting); the file's own values when None."""
        if alpha is None:
            return self.weights
        return {s.id: (alpha * s.F + beta * s.I) / 3 for s in self.shapes}

    @property
    def sum_weights(self) -> float:
        return sum(s.weight for s in self.shapes)

    @property
    def derived_ids(self) -> set[str]:
        return {s.id for s in self.shapes if s.derived}

    def get(self, shape_id: str) -> Shape | None:
        return next((s for s in self.shapes if s.id == shape_id), None)


def load_legend(path: Path) -> Legend:
    data = tomllib.loads(path.read_text())
    alpha, beta = float(data["alpha"]), float(data["beta"])
    shapes = []
    for s in data["shape"]:
        F, I = float(s["F"]), float(s["I"])
        for label, v in (("F", F), ("I", I)):
            if not 1 <= v <= 3:
                raise ValueError(f"shape {s['id']}: {label} must be between 1 and 3, got {v}")
        shapes.append(
            Shape(
                id=s["id"],
                name=s["name"],
                description=s["description"],
                example=s["example"],
                triggers=tuple(s.get("triggers", [])),
                F=F,
                I=I,
                reason=s["reason"],
                derived=bool(s.get("derived", False)),
                weight=(alpha * F + beta * I) / 3,
            )
        )
    ids = [s.id for s in shapes]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate shape ids in legend")
    return Legend(alpha=alpha, beta=beta, repeat_penalty=float(data["repeat_penalty"]), shapes=tuple(shapes))


def render_legend_md(legend: Legend) -> str:
    lines = [
        "| id | name | what it means | trigger words (examples) | example question |",
        "|---|---|---|---|---|",
    ]
    for s in legend.shapes:
        note = " **(derived by code: never link it)**" if s.derived else ""
        lines.append(
            f"| `{s.id}` | {s.name}{note} | {s.description} | {', '.join(s.triggers) or '-'} | {s.example} |"
        )
    return "\n".join(lines)
