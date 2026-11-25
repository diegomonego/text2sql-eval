"""Schema card: everything the LLM needs to know about the database, discovered at run time."""

from __future__ import annotations

from typing import Any

from .db import Database
from .joins import infer_joins

NOTE_CONSTANT = "constant in this data"
NOTE_CODED = "coded: meaning needs docs"


def build_schema_card(db: Database, max_listed_values: int) -> dict[str, Any]:
    tables = db.tables()
    row_counts = {t: db.row_count(t) for t in tables}
    profiles: dict[str, dict[str, dict[str, Any]]] = {}
    for t in tables:
        profiles[t] = {}
        for col, _ in db.columns(t):
            info = db.profile_column(t, col, max_listed_values)
            notes = []
            if row_counts[t] > 0 and info["distinct"] == 1:
                notes.append(NOTE_CONSTANT)
            if (
                info["category"] == "text"
                and info.get("max_length") is not None
                and info["max_length"] <= 2
                and "values" in info
            ):
                notes.append(NOTE_CODED)
            info["notes"] = notes
            profiles[t][col] = info
    joins = infer_joins(db, profiles, row_counts)
    return {
        "database": {"url": db.url, "engine": db.engine, "engine_version": db.engine_version()},
        "tables": [
            {
                "name": t,
                "rows": row_counts[t],
                "columns": [{"name": c, **profiles[t][c]} for c, _ in db.columns(t)],
            }
            for t in tables
        ],
        "joins": joins,
        "eligible": {
            "tables": len(tables),
            "columns": sum(len(db.columns(t)) for t in tables),
        },
    }


def column_index(card: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """'table.column' -> column info (plus 'table')."""
    out = {}
    for t in card["tables"]:
        for c in t["columns"]:
            out[f"{t['name']}.{c['name']}"] = {**c, "table": t["name"]}
    return out


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v)


def render_schema_card_md(card: dict[str, Any], docs_supplied: bool) -> str:
    lines = [
        "# Schema card",
        "",
        f"Engine: {card['database']['engine']} {card['database']['engine_version']}. "
        f"{card['eligible']['tables']} tables, {card['eligible']['columns']} columns. "
        "Discovered from the database catalog and data at run time.",
        "",
    ]
    for t in card["tables"]:
        lines += [f"## {t['name']} ({t['rows']:,} rows)", "", "| column | type | stats | values / samples | notes |", "|---|---|---|---|---|"]
        for c in t["columns"]:
            stats = [f"{c['distinct']:,} distinct"]
            if c.get("nulls"):
                stats.append(f"{c['nulls']:,} nulls")
            if "min" in c:
                stats.append(f"{_fmt(c['min'])} to {_fmt(c['max'])}")
            if c["category"] == "text" and c.get("max_length") is not None:
                stats.append(f"length {c['min_length']}-{c['max_length']}")
            if "values" in c:
                vals = "values: " + ", ".join(f"`{v}`" for v in c["values"])
            elif "samples" in c:
                vals = "e.g. " + ", ".join(f"`{v}`" for v in c["samples"])
            else:
                vals = ""
            notes = list(c["notes"])
            if not docs_supplied and "coded: meaning needs docs" in notes:
                notes = ["coded: meaning needs docs (NO DOCS SUPPLIED: do not use)"]
            lines.append(f"| `{c['name']}` | {c['type']} | {'; '.join(stats)} | {vals} | {'; '.join(notes)} |")
        lines.append("")
    lines += ["## Joins", ""]
    if card["joins"]:
        src = {e["source"] for e in card["joins"]}
        lines.append(
            "Declared foreign keys." if src == {"declared"} else
            "No foreign keys are declared; these were inferred from column names and confirmed against the data."
        )
        lines.append("")
        lines += [f"- `{e['from']}` -> `{e['to']}`" for e in card["joins"]]
    else:
        lines.append("No joins found.")
    lines.append("")
    return "\n".join(lines)
