"""Generation targets: (shape, focus table) pairs plus free slots."""

from __future__ import annotations

from typing import Any

from .config import PoolSettings


def pool_sizes(n: int, pool: PoolSettings) -> tuple[int, int]:
    """(targeted slots, free slots)."""
    return max(pool.targeted_per_n * n, pool.min_targeted), pool.free_per_n * n


def build_targets(
    n: int, shape_ids: list[str], card: dict[str, Any], pool: PoolSettings, focus_tables: bool = True
) -> list[dict[str, str]]:
    """Every shape gets at least 2 targets (with the default sizes); focus tables rotate, largest first,
    shifting by one each round so the same (shape, table) pair doesn't repeat. With focus_tables=False
    (the natural preset) targets name a shape only."""
    if n < 1:
        raise ValueError("N must be a positive integer")
    targeted, free = pool_sizes(n, pool)
    tables = [t["name"] for t in sorted(card["tables"], key=lambda t: (-t["rows"], t["name"]))]
    out = []
    for i in range(targeted):
        shape = shape_ids[i % len(shape_ids)]
        table = tables[(i + i // len(shape_ids)) % len(tables)]
        target = {"id": f"t{i + 1:02d}", "kind": "targeted", "shape": shape}
        if focus_tables:
            target["focus_table"] = table
        out.append(target)
    for j in range(free):
        out.append({"id": f"f{j + 1:02d}", "kind": "free"})
    return out
