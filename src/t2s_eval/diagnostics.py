"""Selection diagnostics written next to each generated question set (generation/diagnostics.json).

They answer, per run:
- what the pool could have covered, against what was selected (the pool is the ceiling);
- how close greedy came to the best subset of the same pool (exact when the subsets are few enough,
  otherwise the best found by single swaps starting from greedy);
- how many picks change under other reasonable settings (sensitivity);
- how many picks came from free-form slots.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from dataclasses import replace
from typing import Any

from .legend import Legend
from .selection import GainSettings, Scored, greedy_select

EXACT_LIMIT = 300_000


def objective(subset: list[Scored] | tuple[Scored, ...], g: GainSettings) -> float:
    """The value greedy maximizes: the sum of the gains of the subset, in any order."""
    counts: dict[str, int] = {}
    tables: set[str] = set()
    columns: set[str] = set()
    for c in subset:
        for s in c.shapes:
            counts[s] = counts.get(s, 0) + 1
        tables |= c.tables
        columns |= c.columns
    shape = sum(g.weights.get(s, 0.0) * sum(g.repeat_penalty**k for k in range(k_s)) for s, k_s in counts.items())
    return (
        (g.lambda_shape * shape / g.sum_weights if g.sum_weights else 0.0)
        + (g.lambda_table * len(tables) / g.n_tables if g.n_tables else 0.0)
        + (g.lambda_column * len(columns) / g.n_columns if g.n_columns else 0.0)
    )


def coverage(subset: list[Scored]) -> dict[str, int]:
    return {
        "tables": len(set().union(*[c.tables for c in subset])) if subset else 0,
        "columns": len(set().union(*[c.columns for c in subset])) if subset else 0,
        "shapes": len(set().union(*[c.shapes for c in subset])) if subset else 0,
    }


def _feasible(subset, min_quota: int, in_quota) -> bool:
    return not min_quota or sum(1 for c in subset if in_quota(c)) >= min_quota


def best_subset(
    cands: list[Scored], picks: list[Scored], g: GainSettings, min_quota: int = 0, in_quota: Callable | None = None
) -> dict[str, Any]:
    n = len(picks)
    n_subsets = math.comb(len(cands), n)
    if n_subsets <= EXACT_LIMIT:
        best, best_v = list(picks), objective(picks, g)
        for sub in itertools.combinations(cands, n):
            if _feasible(sub, min_quota, in_quota):
                v = objective(sub, g)
                if v > best_v + 1e-12:
                    best, best_v = list(sub), v
        method = f"exact, over all {n_subsets:,} subsets"
    else:
        best, best_v = list(picks), objective(picks, g)
        improved = True
        while improved:
            improved = False
            for i in range(n):
                for c in cands:
                    if c in best:
                        continue
                    trial = best[:i] + [c] + best[i + 1 :]
                    if _feasible(trial, min_quota, in_quota):
                        v = objective(trial, g)
                        if v > best_v + 1e-12:
                            best, best_v, improved = trial, v, True
        method = f"best found by single swaps after greedy ({n_subsets:,} subsets is too many to check)"
    greedy_v = objective(picks, g)
    return {
        "greedy_value": round(greedy_v, 4),
        "best_value": round(best_v, 4),
        "greedy_over_best": round(greedy_v / best_v, 4) if best_v else 1.0,
        "method": method,
        "picks_that_differ": sorted({c.id for c in best} ^ {c.id for c in picks}),
    }


def sensitivity(
    cands: list[Scored],
    picks: list[Scored],
    g: GainSettings,
    legend: Legend,
    alpha: float,
    beta: float,
    min_quota: int = 0,
    in_quota: Callable | None = None,
) -> dict[str, Any]:
    """How many of the N picks change under other settings, everything else held equal."""
    n = len(picks)
    base = {c.id for c in picks}

    def changed(gs: GainSettings) -> int:
        return len(base - {c.id for c in greedy_select(cands, n, gs, min_quota, in_quota)[0]})

    variants = {
        "lambdas in equal thirds": replace(g, lambda_shape=1 / 3, lambda_table=1 / 3, lambda_column=1 / 3),
        "lambda_column = 0.5": replace(g, lambda_shape=0.25, lambda_table=0.25, lambda_column=0.5),
        "repeat factor 0.3": replace(g, repeat_penalty=0.3),
        "repeat factor 0.7": replace(g, repeat_penalty=0.7),
        "W = F x I / 9 (multiplied, not added)": replace(g, weights={s.id: s.F * s.I / 9 for s in legend.shapes}),
        "no F (alpha = 0)": replace(g, weights={s.id: s.I / 3 for s in legend.shapes}),
    }
    out: dict[str, Any] = {name: changed(gs) for name, gs in variants.items()}
    nudges = []
    for s in legend.shapes:
        for attr in ("F", "I"):
            for d in (-1, 1):
                v = getattr(s, attr) + d
                if not 1 <= v <= 3:
                    continue
                F = v if attr == "F" else s.F
                I = v if attr == "I" else s.I
                w = dict(g.weights)
                w[s.id] = (alpha * F + beta * I) / 3
                nudges.append(changed(replace(g, weights=w)))
    out["each F or I nudged by 1"] = {
        "variants": len(nudges),
        "max_changed": max(nudges) if nudges else 0,
        "mean_changed": round(sum(nudges) / len(nudges), 2) if nudges else 0,
        "unchanged": nudges.count(0),
    }
    return out


def selection_diagnostics(
    cands: list[Scored],
    picks: list[Scored],
    g: GainSettings,
    legend: Legend,
    alpha: float,
    beta: float,
    is_free: Callable[[Scored], bool],
    min_quota: int = 0,
) -> dict[str, Any]:
    in_quota = is_free if min_quota else None
    return {
        "pool_ceiling": {"pool": coverage(cands), "selected": coverage(picks), "valid_unique_candidates": len(cands)},
        "greedy_vs_best": best_subset(cands, picks, g, min_quota, in_quota),
        "sensitivity_picks_changed": sensitivity(cands, picks, g, legend, alpha, beta, min_quota, in_quota),
        "free_form": {
            "picks": sum(1 for c in picks if is_free(c)),
            "of": len(picks),
            "in_pool": sum(1 for c in cands if is_free(c)),
            "pool": len(cands),
            "required": min_quota,
        },
    }
