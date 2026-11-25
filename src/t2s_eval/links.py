"""Quoted-phrase links and the code that checks them.

The LLM (generator or judge) quotes phrases from a question and links each one to a table,
column(s) (optionally with a value), a shape, or marks it as a concept the database lacks.
Nothing here trusts the LLM: every link is checked against the question text, the catalog,
the data and the shape legend, and the linked tables must connect through the join graph.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .db import Database
from .joins import adjacency, connect_tables
from .legend import Legend
from .schema_card import NOTE_CODED, column_index

JOIN_SHAPE = "multi_join"


class Link(BaseModel):
    model_config = ConfigDict(extra="ignore")

    phrase: str
    kind: Literal["table", "column", "shape", "missing"]
    table: str | None = None
    columns: list[str] = Field(default_factory=list)
    value: str | int | float | None = None
    match: Literal["exact", "contains"] = "exact"
    shape: str | None = None
    source: str | None = None
    alternatives: list[list[str]] = Field(default_factory=list)
    concept: str | None = None
    closest: list[str] = Field(default_factory=list)
    why_not: str | None = None


@dataclass
class LinkCheck:
    ok: bool
    problems: list[str] = field(default_factory=list)
    ignored: bool = False


@dataclass
class Analysis:
    link_checks: list[LinkCheck]
    tables: set[str]
    columns: set[str]
    shapes: set[str]
    ambiguous: list[dict[str, Any]]
    missing: list[dict[str, Any]]
    connected: bool
    path_tables: list[str]

    @property
    def all_links_ok(self) -> bool:
        return all(c.ok for c in self.link_checks)

    @property
    def failed(self) -> list[tuple[int, LinkCheck]]:
        return [(i, c) for i, c in enumerate(self.link_checks) if not c.ok]


# ---------------------------------------------------------------- phrase matching

_TRANS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.translate(_TRANS).lower()).strip()


def phrase_in_question(phrase: str, question: str) -> bool:
    """Case-insensitive; '…' or '...' in the phrase joins parts that must appear in order."""
    q = _norm(question)
    parts = [p.strip(" ,.;:?!\"'") for p in re.split(r"\s*(?:…|\.\.\.)\s*", _norm(phrase))]
    parts = [p for p in parts if p]
    if not parts:
        return False
    pos = 0
    for p in parts:
        i = q.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


# ---------------------------------------------------------------- value checks

_QUARTER = re.compile(r"^(\d{4})-?Q([1-4])$", re.I)


def parse_date_spec(spec: str) -> tuple[dt.date, dt.date]:
    """'1997', '1997-03', '1997-03-15', '1997-Q2', or 'A..B' with any of those -> (start, end)."""
    spec = spec.strip()
    if ".." in spec:
        a, b = spec.split("..", 1)
        return parse_date_spec(a)[0], parse_date_spec(b)[1]
    m = _QUARTER.match(spec)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        start = dt.date(y, 3 * (q - 1) + 1, 1)
        nxt = dt.date(y + 1, 1, 1) if q == 4 else dt.date(y, 3 * q + 1, 1)
        return start, nxt - dt.timedelta(days=1)
    if re.fullmatch(r"\d{4}", spec):
        y = int(spec)
        return dt.date(y, 1, 1), dt.date(y, 12, 31)
    if re.fullmatch(r"\d{4}-\d{2}", spec):
        y, m_ = map(int, spec.split("-"))
        start = dt.date(y, m_, 1)
        nxt = dt.date(y + 1, 1, 1) if m_ == 12 else dt.date(y, m_ + 1, 1)
        return start, nxt - dt.timedelta(days=1)
    d = dt.date.fromisoformat(spec[:10])
    return d, d


def _parse_number(s: str) -> float:
    return float(s.strip().replace(",", "").replace("$", ""))


def check_value(info: dict[str, Any], value: str, match: str, db: Database) -> str | None:
    """Return a problem description, or None when the value is plausible for the column."""
    cat = info["category"]
    if cat == "date":
        try:
            start, end = parse_date_spec(value)
        except (ValueError, IndexError):
            return f"date value '{value}' must be YYYY, YYYY-MM, YYYY-MM-DD, YYYY-Qn or A..B"
        lo, hi = dt.date.fromisoformat(str(info["min"])[:10]), dt.date.fromisoformat(str(info["max"])[:10])
        if start > hi or end < lo:
            return f"date '{value}' is outside the data's range ({lo} to {hi})"
        return None
    if cat == "number":
        try:
            parts = [_parse_number(p) for p in value.split("..")] if ".." in value else [_parse_number(value)]
        except ValueError:
            return f"number value '{value}' is not a number (use stored units, e.g. 0.05 not 5%)"
        lo, hi = float(info["min"]), float(info["max"])
        if max(parts) < lo or min(parts) > hi:
            return f"number '{value}' is outside the data's range ({lo:g} to {hi:g})"
        return None
    if cat == "text":
        if not db.value_exists(info["table"], info["name"], value, match):
            how = "contained in any value" if match == "contains" else "an existing value"
            return f"'{value}' is not {how} of {info['table']}.{info['name']}"
        return None
    return None


# ---------------------------------------------------------------- the checker


class LinkChecker:
    def __init__(self, card: dict[str, Any], db: Database, legend: Legend) -> None:
        self.card = card
        self.db = db
        self.legend = legend
        self.cols = column_index(card)
        self.tables = {t["name"] for t in card["tables"]}
        self.adj = adjacency(card["joins"])

    def _column_problem(self, ref: str) -> str | None:
        if ref.count(".") != 1:
            return f"column '{ref}' must be written as table.column"
        if ref not in self.cols:
            return f"column '{ref}' does not exist"
        return None

    def check_link(self, link: Link, question: str) -> LinkCheck:
        problems: list[str] = []
        if not phrase_in_question(link.phrase, question):
            problems.append(f"phrase '{link.phrase}' does not appear in the question")
        if link.kind == "table":
            if not link.table:
                problems.append("table link without 'table'")
            elif link.table not in self.tables:
                problems.append(f"table '{link.table}' does not exist")
        elif link.kind == "column":
            if not link.columns:
                problems.append("column link without 'columns'")
            for ref in link.columns:
                p = self._column_problem(ref)
                if p:
                    problems.append(p)
            for alt in link.alternatives:
                for ref in alt:
                    p = self._column_problem(ref)
                    if p:
                        problems.append(f"alternative: {p}")
            if link.value not in (None, "") and link.columns and not problems:
                p = check_value(self.cols[link.columns[0]], str(link.value), link.match, self.db)
                if p:
                    problems.append(p)
        elif link.kind == "shape":
            if not link.shape:
                problems.append("shape link without 'shape'")
            elif self.legend.get(link.shape) is None:
                problems.append(f"shape '{link.shape}' is not in the legend")
            elif link.shape in self.legend.derived_ids:
                return LinkCheck(ok=True, problems=[f"'{link.shape}' is derived by code; link ignored"], ignored=True)
        elif link.kind == "missing":
            if not (link.concept or "").strip():
                problems.append("missing link without 'concept'")
            for ref in link.closest:
                p = self._column_problem(ref)
                if p:
                    problems.append(f"closest: {p}")
        return LinkCheck(ok=not problems, problems=problems)

    def analyze(self, question: str, links: list[Link]) -> Analysis:
        checks = [self.check_link(l, question) for l in links]
        tables: set[str] = set()
        columns: set[str] = set()
        shapes: set[str] = set()
        ambiguous: list[dict[str, Any]] = []
        missing: list[dict[str, Any]] = []
        connect: set[str] = set()
        for link, chk in zip(links, checks):
            if link.kind == "missing":
                missing.append({"phrase": link.phrase, "concept": link.concept, "closest": link.closest, "why_not": link.why_not})
                continue
            if not chk.ok or chk.ignored:
                continue
            if link.kind == "table":
                tables.add(link.table)
                connect.add(link.table)
            elif link.kind == "column":
                link_tables = {c.split(".", 1)[0] for c in link.columns}
                connect |= link_tables
                if link.alternatives:
                    ambiguous.append({"phrase": link.phrase, "readings": [link.columns, *link.alternatives]})
                else:
                    columns |= set(link.columns)
                    tables |= link_tables
            elif link.kind == "shape":
                shapes.add(link.shape)
        connected, path = connect_tables(connect, self.adj)
        if connected and len(path) >= 3 and JOIN_SHAPE in self.legend.ids:
            shapes.add(JOIN_SHAPE)
        return Analysis(checks, tables, columns, shapes, ambiguous, missing, connected, path)

    def coded_columns(self) -> set[str]:
        return {ref for ref, info in self.cols.items() if NOTE_CODED in info["notes"]}


def link_record(link: Link, chk: LinkCheck) -> dict[str, Any]:
    """A link plus its check result, as stored in reports."""
    rec = link.model_dump(exclude_defaults=True)
    rec["check"] = "ignored" if chk.ignored else ("pass" if chk.ok else "fail")
    if chk.problems:
        rec["problems"] = chk.problems
    return rec


def label_check(labels: dict[str, list[str]] | None, analysis: Analysis) -> list[dict[str, str]]:
    """Compare a question's labels (claims) with what the judge's own links support."""
    found = {"tables": analysis.tables, "columns": analysis.columns, "shapes": analysis.shapes}
    out = []
    labels = labels or {}
    for dim in ("tables", "columns", "shapes"):
        claimed = set(labels.get(dim, []))
        for item in sorted(claimed):
            out.append({"dimension": dim, "item": item, "status": "confirmed" if item in found[dim] else "not supported"})
        if labels:
            for item in sorted(found[dim] - claimed):
                out.append({"dimension": dim, "item": item, "status": "not labeled"})
    return out
