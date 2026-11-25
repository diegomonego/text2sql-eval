"""Duplicate removal and greedy selection of exactly N questions (pure logic, no I/O)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Scored:
    """A valid candidate with the items it earns credit for."""

    id: str
    tables: frozenset[str]
    columns: frozenset[str]
    shapes: frozenset[str]
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def signature(self) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
        """Same tables, columns and shapes = same computation (filter values are ignored)."""
        return self.tables, self.columns, self.shapes


def dedupe(cands: list[Scored]) -> tuple[list[Scored], dict[str, str]]:
    """Keep the first candidate of each signature. Returns (unique, {duplicate id: kept id})."""
    seen: dict[tuple, str] = {}
    unique, dups = [], {}
    for c in cands:
        if c.signature in seen:
            dups[c.id] = seen[c.signature]
        else:
            seen[c.signature] = c.id
            unique.append(c)
    return unique, dups


@dataclass(frozen=True)
class GainSettings:
    weights: dict[str, float]
    repeat_penalty: float
    lambda_shape: float
    lambda_table: float
    lambda_column: float
    n_tables: int
    n_columns: int

    @property
    def sum_weights(self) -> float:
        return sum(self.weights.values())


def gain_parts(c: Scored, shape_counts: dict[str, int], tables: set[str], columns: set[str], g: GainSettings) -> dict[str, float]:
    shape_gain = sum(g.weights.get(s, 0.0) * g.repeat_penalty ** shape_counts.get(s, 0) for s in c.shapes)
    parts = {
        "shape": g.lambda_shape * shape_gain / g.sum_weights if g.sum_weights else 0.0,
        "table": g.lambda_table * len(c.tables - tables) / g.n_tables if g.n_tables else 0.0,
        "column": g.lambda_column * len(c.columns - columns) / g.n_columns if g.n_columns else 0.0,
    }
    parts["total"] = parts["shape"] + parts["table"] + parts["column"]
    return parts


class NotEnoughCandidates(Exception):
    pass


def greedy_select(
    cands: list[Scored],
    n: int,
    g: GainSettings,
    min_quota: int = 0,
    in_quota: Callable[[Scored], bool] | None = None,
) -> tuple[list[Scored], list[dict[str, Any]]]:
    """Pick exactly n candidates, one per round, by largest marginal gain (ties: earliest candidate).

    With min_quota > 0, at least that many picks must satisfy in_quota (the natural preset's free-form
    share): once the slots left equal the unmet quota, only quota candidates may be picked. That is a
    matroid constraint (at most n - min_quota other picks), under which greedy keeps a 1/2 guarantee
    (Fisher, Nemhauser & Wolsey 1978, Mathematical Programming Studies 8:73-87, doi:10.1007/BFb0121195).
    Without a quota the objective is monotone submodular and greedy is within 1 - 1/e of the best subset
    (Nemhauser, Wolsey & Fisher 1978, Mathematical Programming 14:265-294, doi:10.1007/BF01588971).
    """
    if len(cands) < n:
        raise NotEnoughCandidates(f"{len(cands)} valid unique candidates, {n} needed")
    min_quota = min(min_quota, n)
    if min_quota and in_quota is None:
        raise ValueError("min_quota needs an in_quota predicate")
    eligible = sum(1 for c in cands if in_quota(c)) if min_quota else 0
    if eligible < min_quota:
        raise NotEnoughCandidates(f"{eligible} valid unique free-form candidates, at least {min_quota} needed")
    picked: list[Scored] = []
    shape_counts: dict[str, int] = {}
    tables: set[str] = set()
    columns: set[str] = set()
    log = []
    remaining = list(cands)
    for rnd in range(1, n + 1):
        unmet = max(0, min_quota - sum(1 for c in picked if in_quota(c))) if min_quota else 0
        restricted = unmet > 0 and unmet >= n - len(picked)
        pool = [c for c in remaining if in_quota(c)] if restricted else remaining
        scored = [(c, gain_parts(c, shape_counts, tables, columns, g)) for c in pool]
        best_c, best_p = scored[0]
        for c, p in scored[1:]:
            if p["total"] > best_p["total"] + 1e-12:
                best_c, best_p = c, p
        log.append(
            {
                "round": rnd,
                "picked": best_c.id,
                **({"restricted_to_quota": True} if restricted else {}),
                "gain": {k: round(v, 6) for k, v in best_p.items()},
                "candidates": [
                    {"id": c.id, **{k: round(v, 6) for k, v in p.items()}}
                    for c, p in sorted(scored, key=lambda cp: -cp[1]["total"])
                ],
            }
        )
        picked.append(best_c)
        remaining.remove(best_c)
        for s in best_c.shapes:
            shape_counts[s] = shape_counts.get(s, 0) + 1
        tables |= best_c.tables
        columns |= best_c.columns
    return picked, log
