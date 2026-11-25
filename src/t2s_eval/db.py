"""Database access behind one small interface.

Everything else in the package talks to `Database`, never to an engine directly.
Adding an engine (e.g. Postgres) means writing one subclass and registering its URL
scheme in CONNECTORS.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

APPROX_DISTINCT_ABOVE_ROWS = 1_000_000
MAX_LISTED_NON_TEXT = 10  # numbers and dates: list values only when there are very few

TEXT_TYPES = ("VARCHAR", "CHAR", "TEXT", "STRING", "BPCHAR")
DATE_TYPES = ("DATE", "TIMESTAMP", "TIME")
NUMBER_TYPES = ("INT", "DECIMAL", "NUMERIC", "DOUBLE", "FLOAT", "REAL", "BIGINT", "SMALLINT", "TINYINT", "HUGEINT")


def type_category(sql_type: str) -> str:
    t = sql_type.upper()
    if t.startswith(DATE_TYPES):
        return "date"
    if t.startswith(TEXT_TYPES):
        return "text"
    if any(t.startswith(n) or n in t for n in NUMBER_TYPES):
        return "number"
    return "other"


class Database(ABC):
    """Read-only access to a relational database."""

    engine: str = "unknown"

    def __init__(self, url: str) -> None:
        self.url = url

    @abstractmethod
    def tables(self) -> list[str]: ...

    @abstractmethod
    def columns(self, table: str) -> list[tuple[str, str]]:
        """(column name, SQL type) in table order."""

    @abstractmethod
    def declared_foreign_keys(self) -> list[tuple[str, str, str, str]]:
        """(table, column, referenced table, referenced column) for single-column foreign keys."""

    @abstractmethod
    def row_count(self, table: str) -> int: ...

    @abstractmethod
    def profile_column(self, table: str, column: str, max_values: int) -> dict[str, Any]:
        """Distinct count, nulls, min/max (and text lengths), values when few, a few samples otherwise."""

    @abstractmethod
    def value_exists(self, table: str, column: str, value: str, match: str = "exact") -> bool:
        """Case-insensitive check that a text value exists (exact match, or contained in a value)."""

    @abstractmethod
    def contained_in(self, table: str, column: str, ref_table: str, ref_column: str) -> bool:
        """True when every non-null value of table.column exists in ref_table.ref_column."""

    @abstractmethod
    def engine_version(self) -> str: ...

    def file_path(self) -> Path | None:
        return None

    def fingerprint(self) -> dict[str, Any]:
        path = self.file_path()
        sha = None
        if path and path.is_file():
            h = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            sha = h.hexdigest()
        tables = self.tables()
        return {
            "url": self.url,
            "engine": self.engine,
            "engine_version": self.engine_version(),
            "file_sha256": sha,
            "tables": len(tables),
            "columns": sum(len(self.columns(t)) for t in tables),
        }

    def close(self) -> None:  # pragma: no cover - trivial
        pass


class DuckDBDatabase(Database):
    engine = "duckdb"

    def __init__(self, url: str, path: Path) -> None:
        super().__init__(url)
        import duckdb

        if not path.is_file():
            raise FileNotFoundError(f"database file not found: {path} (run `make db`)")
        self._path = path
        self._con = duckdb.connect(str(path), read_only=True)
        self._duckdb_version = duckdb.__version__
        self._catalog: dict[str, list[tuple[str, str]]] = {}
        rows = self._con.execute(
            "SELECT table_name, column_name, data_type FROM information_schema.columns "
            "WHERE table_schema = 'main' ORDER BY table_name, ordinal_position"
        ).fetchall()
        for t, c, ty in rows:
            self._catalog.setdefault(t, []).append((c, ty))

    # identifiers are only ever taken from the catalog, then quoted
    def _q(self, table: str, column: str | None = None) -> str:
        if table not in self._catalog:
            raise KeyError(f"unknown table: {table}")
        if column is not None and column not in {c for c, _ in self._catalog[table]}:
            raise KeyError(f"unknown column: {table}.{column}")
        qt = '"' + table.replace('"', '""') + '"'
        return qt if column is None else '"' + column.replace('"', '""') + '"'

    def tables(self) -> list[str]:
        return sorted(self._catalog)

    def columns(self, table: str) -> list[tuple[str, str]]:
        self._q(table)
        return list(self._catalog[table])

    def declared_foreign_keys(self) -> list[tuple[str, str, str, str]]:
        out = []
        rows = self._con.execute(
            "SELECT table_name, constraint_column_names, referenced_table, referenced_column_names "
            "FROM duckdb_constraints() WHERE constraint_type = 'FOREIGN KEY'"
        ).fetchall()
        for table, cols, ref_table, ref_cols in rows:
            if cols and ref_cols and len(cols) == 1 and len(ref_cols) == 1:
                out.append((table, cols[0], ref_table, ref_cols[0]))
        return out

    def row_count(self, table: str) -> int:
        return self._con.execute(f"SELECT count(*) FROM {self._q(table)}").fetchone()[0]

    def profile_column(self, table: str, column: str, max_values: int) -> dict[str, Any]:
        t, c = self._q(table), self._q(table, column)
        sql_type = dict(self._catalog[table])[column]
        cat = type_category(sql_type)
        approximate = self.row_count(table) > APPROX_DISTINCT_ABOVE_ROWS
        distinct_expr = f"approx_count_distinct({c})" if approximate else f"count(DISTINCT {c})"
        nulls, distinct = self._con.execute(
            f"SELECT count(*) - count({c}), {distinct_expr} FROM {t}"
        ).fetchone()
        info: dict[str, Any] = {
            "type": sql_type,
            "category": cat,
            "distinct": int(distinct),
            "distinct_is_approximate": approximate,
            "nulls": int(nulls),
        }
        if cat in ("number", "date"):
            lo, hi = self._con.execute(f"SELECT min({c}), max({c}) FROM {t}").fetchone()
            info["min"], info["max"] = _plain(lo), _plain(hi)
        if cat == "text":
            lo, hi = self._con.execute(f"SELECT min(length({c})), max(length({c})) FROM {t}").fetchone()
            info["min_length"], info["max_length"] = lo, hi
        listed_limit = max_values if cat == "text" else min(max_values, MAX_LISTED_NON_TEXT)
        if distinct <= listed_limit:
            vals = self._con.execute(f"SELECT DISTINCT {c} FROM {t} WHERE {c} IS NOT NULL ORDER BY 1").fetchall()
            info["values"] = [_plain(v[0]) for v in vals]
        elif cat == "text":
            vals = self._con.execute(f"SELECT DISTINCT {c} FROM {t} WHERE {c} IS NOT NULL ORDER BY 1 LIMIT 3").fetchall()
            info["samples"] = [_plain(v[0]) for v in vals]
        return info

    def value_exists(self, table: str, column: str, value: str, match: str = "exact") -> bool:
        t, c = self._q(table), self._q(table, column)
        if match == "contains":
            sql = f"SELECT 1 FROM {t} WHERE contains(lower(CAST({c} AS VARCHAR)), lower(?)) LIMIT 1"
            param = value
        else:
            sql = f"SELECT 1 FROM {t} WHERE lower(CAST({c} AS VARCHAR)) = lower(?) LIMIT 1"
            param = value
        return self._con.execute(sql, [param]).fetchone() is not None

    def contained_in(self, table: str, column: str, ref_table: str, ref_column: str) -> bool:
        t, c = self._q(table), self._q(table, column)
        rt, rc = self._q(ref_table), self._q(ref_table, ref_column)
        missing = self._con.execute(
            f"SELECT count(*) FROM {t} a WHERE a.{c} IS NOT NULL "
            f"AND NOT EXISTS (SELECT 1 FROM {rt} b WHERE b.{rc} = a.{c})"
        ).fetchone()[0]
        return missing == 0

    def engine_version(self) -> str:
        return self._duckdb_version

    def file_path(self) -> Path | None:
        return self._path

    def max_value(self, table: str, column: str) -> Any:
        t, c = self._q(table), self._q(table, column)
        return _plain(self._con.execute(f"SELECT max({c}) FROM {t}").fetchone()[0])

    def close(self) -> None:
        self._con.close()


def _plain(v: Any) -> Any:
    """Convert database values to JSON-friendly Python values."""
    import datetime
    import decimal

    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    return v


def _duckdb_from_url(url: str, root: Path) -> Database:
    rest = url.split("://", 1)[1]
    # duckdb:///relative/path.duckdb is relative to the repo root; duckdb:////abs/path is absolute
    path = Path(rest[1:]) if rest.startswith("/") else Path(rest)
    if not path.is_absolute():
        path = root / path
    return DuckDBDatabase(url, path)


CONNECTORS = {"duckdb": _duckdb_from_url}


def connect(url: str, root: Path) -> Database:
    scheme = url.split("://", 1)[0].lower()
    if scheme not in CONNECTORS:
        raise ValueError(f"no connector for '{scheme}://' (available: {', '.join(sorted(CONNECTORS))})")
    return CONNECTORS[scheme](url, root)
