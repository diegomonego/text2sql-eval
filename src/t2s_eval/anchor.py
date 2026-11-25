"""Time anchor: the reference date that relative phrases ("last quarter") resolve against."""

from __future__ import annotations

import datetime as dt
from typing import Any


def _quarter_start(d: dt.date) -> dt.date:
    return dt.date(d.year, 3 * ((d.month - 1) // 3) + 1, 1)


def _prev_quarter(d: dt.date) -> tuple[dt.date, dt.date]:
    start = _quarter_start(d)
    end = start - dt.timedelta(days=1)
    return _quarter_start(end), end


def _quarter_label(d: dt.date) -> str:
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def resolve_anchor(mode: str, column: str | None, db: Any | None) -> dict[str, Any]:
    """mode is "auto" (latest value of `column`), "off", or a fixed ISO date."""
    mode = (mode or "off").strip().lower()
    if mode == "off" or (mode == "auto" and not column):
        return {"mode": "off", "column": column, "date": None, "ranges": {}}
    if mode == "auto":
        table, col = column.split(".", 1)
        raw = db.max_value(table, col)
        date = dt.date.fromisoformat(str(raw)[:10])
    else:
        date = dt.date.fromisoformat(mode)
    lq_start, lq_end = _prev_quarter(date)
    month_start = date.replace(day=1)
    lm_end = month_start - dt.timedelta(days=1)
    try:
        year_ago = date.replace(year=date.year - 1)
    except ValueError:  # 29 February
        year_ago = date.replace(year=date.year - 1, day=28)
    ranges = {
        "this year": (dt.date(date.year, 1, 1), date),
        "last year": (dt.date(date.year - 1, 1, 1), dt.date(date.year - 1, 12, 31)),
        "this quarter": (_quarter_start(date), date),
        "last quarter": (lq_start, lq_end),
        "this month": (month_start, date),
        "last month": (lm_end.replace(day=1), lm_end),
        "last 12 months": (year_ago + dt.timedelta(days=1), date),
    }
    labels = {
        "this year": str(date.year),
        "last year": str(date.year - 1),
        "this quarter": _quarter_label(date),
        "last quarter": _quarter_label(lq_start),
        "this month": date.strftime("%Y-%m"),
        "last month": lm_end.strftime("%Y-%m"),
        "last 12 months": f"{(year_ago + dt.timedelta(days=1)).isoformat()}..{date.isoformat()}",
    }
    return {
        "mode": "auto" if mode == "auto" else "fixed",
        "column": column,
        "date": date.isoformat(),
        "ranges": {k: {"from": a.isoformat(), "to": b.isoformat(), "value": labels[k]} for k, (a, b) in ranges.items()},
    }


def render_anchor_md(anchor: dict[str, Any]) -> str:
    if anchor["mode"] == "off":
        return (
            "**Time anchor: OFF.** There is no reference date. Relative time phrases "
            '("last quarter", "this year", "recently") have no fixed meaning: the generator must use '
            "absolute periods only, and judges treat relative-time questions as AMBIGUOUS."
        )
    src = f"the latest `{anchor['column']}`" if anchor["mode"] == "auto" else "a fixed date in the config"
    lines = [
        f"**Time anchor: ON, {anchor['date']}** ({src}). Relative phrases resolve as follows; "
        "use the value column as the link value:",
        "",
        "| phrase | from | to | link value |",
        "|---|---|---|---|",
    ]
    for k, r in anchor["ranges"].items():
        lines.append(f"| {k} | {r['from']} | {r['to']} | `{r['value']}` |")
    return "\n".join(lines)
