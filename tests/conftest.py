"""Shared fixtures: a tiny TPC-H-like database and a throwaway project folder around it."""

from __future__ import annotations

import shutil
from pathlib import Path

import duckdb
import pytest

from t2s_eval.config import load_config
from t2s_eval.db import connect
from t2s_eval.legend import load_legend
from t2s_eval.links import LinkChecker
from t2s_eval.schema_card import build_schema_card

ROOT = Path(__file__).resolve().parents[1]

MINI_SQL = """
CREATE TABLE region (r_regionkey INTEGER, r_name VARCHAR);
INSERT INTO region VALUES (0, 'AFRICA'), (1, 'EUROPE');
CREATE TABLE nation (n_nationkey INTEGER, n_name VARCHAR, n_regionkey INTEGER);
INSERT INTO nation VALUES (0, 'ALGERIA', 0), (1, 'FRANCE', 1), (2, 'GERMANY', 1);
CREATE TABLE customer (c_custkey INTEGER, c_name VARCHAR, c_nationkey INTEGER, c_mktsegment VARCHAR,
                       c_acctbal DECIMAL(15,2), c_flag VARCHAR, c_const INTEGER);
INSERT INTO customer VALUES
  (1, 'Customer#1', 0, 'BUILDING', 100.50, 'A', 0),
  (2, 'Customer#2', 1, 'MACHINERY', -20.00, 'B', 0),
  (3, 'Customer#3', 2, 'BUILDING', 5000.00, 'A', 0),
  (4, 'Customer#4', 1, 'HOUSEHOLD', 10.00, 'B', 0);
CREATE TABLE orders (o_orderkey INTEGER, o_custkey INTEGER, o_orderdate DATE, o_totalprice DECIMAL(15,2),
                     o_orderpriority VARCHAR);
INSERT INTO orders VALUES
  (10, 1, '1995-01-15', 1000.00, '1-URGENT'),
  (11, 1, '1996-03-02', 250.00, '5-LOW'),
  (12, 2, '1997-07-30', 75.25, '1-URGENT'),
  (13, 3, '1998-08-02', 300.00, '3-MEDIUM');
"""


@pytest.fixture(autouse=True)
def _no_claude_subprocess(monkeypatch):
    monkeypatch.setattr("t2s_eval.meta._claude_version", lambda: "test")


@pytest.fixture
def mini_db_path(tmp_path: Path) -> Path:
    path = tmp_path / "mini.duckdb"
    con = duckdb.connect(str(path))
    con.execute(MINI_SQL)
    con.close()
    return path


@pytest.fixture
def project(tmp_path: Path, mini_db_path: Path):
    """A project folder with config pointing at the mini database, the real shape legend and one doc."""
    root = tmp_path / "proj"
    (root / "config").mkdir(parents=True)
    shutil.copy(ROOT / "config" / "shapes.toml", root / "config" / "shapes.toml")
    eval_toml = (ROOT / "config" / "eval.toml").read_text()
    eval_toml = eval_toml.replace('url = "duckdb:///data/tpch_sf01.duckdb"', f'url = "duckdb:///{mini_db_path}"')
    eval_toml = eval_toml.replace('dir = "semantic_docs/tpch"', 'dir = "docs"')
    (root / "config" / "eval.toml").write_text(eval_toml)
    (root / "docs").mkdir()
    (root / "docs" / "glossary.md").write_text("# Glossary\n\nOrder value = o_totalprice.\n")
    return load_config(root)


@pytest.fixture
def mini_db(project):
    db = connect(project.db_url, project.root)
    yield db
    db.close()


@pytest.fixture
def legend():
    return load_legend(ROOT / "config" / "shapes.toml")


@pytest.fixture
def card(mini_db):
    return build_schema_card(mini_db, 25)


@pytest.fixture
def checker(card, mini_db, legend):
    return LinkChecker(card, mini_db, legend)
