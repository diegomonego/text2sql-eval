"""Join discovery and path search over the join graph."""

from __future__ import annotations

from collections import deque
from typing import Any

MIN_SUFFIX = 3


def _suffix(column: str) -> str:
    """Column name without its table prefix: o_custkey -> custkey, ss_sold_date_sk -> sold_date_sk."""
    return column.split("_", 1)[1] if "_" in column else column


def infer_joins(db: Any, profiles: dict[str, dict[str, dict[str, Any]]], row_counts: dict[str, int]) -> list[dict[str, str]]:
    """Declared single-column foreign keys when the database has any; otherwise inferred ones.

    Inference: a column `a` in table T1 joins to a unique, non-null column `b` in table T2 when
    the name of `a` (without its prefix) ends with the name of `b` (without its prefix), both have
    the same kind of type, and every value of `a` exists in `b` (checked against the data).
    """
    declared = db.declared_foreign_keys()
    if declared:
        return [
            {"from": f"{t}.{c}", "to": f"{rt}.{rc}", "source": "declared"}
            for t, c, rt, rc in sorted(declared)
        ]
    keys = []  # unique, non-null columns
    for table, cols in profiles.items():
        n = row_counts.get(table, 0)
        for col, info in cols.items():
            if n > 0 and info["nulls"] == 0 and info["distinct"] == n and not info.get("distinct_is_approximate"):
                keys.append((table, col, info["category"]))
    edges = []
    for kt, kc, kcat in keys:
        ksuf = _suffix(kc)
        if len(ksuf) < MIN_SUFFIX:
            continue
        for table, cols in profiles.items():
            if table == kt:
                continue
            for col, info in cols.items():
                if info["category"] != kcat or not _suffix(col).endswith(ksuf):
                    continue
                if db.contained_in(table, col, kt, kc):
                    edges.append({"from": f"{table}.{col}", "to": f"{kt}.{kc}", "source": "inferred"})
    edges.sort(key=lambda e: (e["from"], e["to"]))
    return edges


def adjacency(joins: list[dict[str, str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {}
    for e in joins:
        a, b = e["from"].split(".", 1)[0], e["to"].split(".", 1)[0]
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def connect_tables(tables: set[str] | list[str], adj: dict[str, set[str]]) -> tuple[bool, list[str]]:
    """Connect the given tables through the join graph.

    Returns (connected, tables on the connecting paths). Greedy and deterministic: start from the
    alphabetically first table and repeatedly attach the nearest unconnected table by a shortest path.
    """
    wanted = sorted(set(tables))
    if len(wanted) <= 1:
        return True, wanted
    tree = {wanted[0]}
    remaining = set(wanted[1:])
    while remaining:
        prev: dict[str, str | None] = {t: None for t in tree}
        queue = deque(sorted(tree))
        found = None
        while queue:
            cur = queue.popleft()
            if cur in remaining:
                found = cur
                break
            for nb in sorted(adj.get(cur, ())):
                if nb not in prev:
                    prev[nb] = cur
                    queue.append(nb)
        if found is None:
            return False, sorted(tree | remaining)
        node: str | None = found
        while node is not None and node not in tree:
            tree.add(node)
            node = prev[node]
        remaining -= tree
    return True, sorted(tree)
