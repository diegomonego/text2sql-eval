import pytest

from t2s_eval.db import connect
from t2s_eval.schema_card import NOTE_CODED, NOTE_CONSTANT, column_index, render_schema_card_md


def test_catalog_and_profile(mini_db):
    assert mini_db.tables() == ["customer", "nation", "orders", "region"]
    assert [c for c, _ in mini_db.columns("region")] == ["r_regionkey", "r_name"]
    assert mini_db.row_count("customer") == 4
    prof = mini_db.profile_column("orders", "o_orderdate", 25)
    assert prof["category"] == "date" and prof["min"] == "1995-01-15" and prof["max"] == "1998-08-02"
    seg = mini_db.profile_column("customer", "c_mktsegment", 25)
    assert seg["values"] == ["BUILDING", "HOUSEHOLD", "MACHINERY"]


def test_value_exists_is_case_insensitive_and_supports_contains(mini_db):
    assert mini_db.value_exists("region", "r_name", "Europe")
    assert not mini_db.value_exists("region", "r_name", "ASIA")
    assert mini_db.value_exists("customer", "c_name", "omer#3", match="contains")
    assert not mini_db.value_exists("customer", "c_name", "omer#9", match="contains")


def test_identifiers_must_come_from_the_catalog(mini_db):
    with pytest.raises(KeyError):
        mini_db.row_count('region"; DROP TABLE region; --')
    with pytest.raises(KeyError):
        mini_db.value_exists("region", "nope", "x")


def test_unknown_scheme_is_rejected(project):
    with pytest.raises(ValueError, match="no connector"):
        connect("postgresql://localhost/db", project.root)


def test_joins_inferred_from_names_and_data(card):
    edges = {(e["from"], e["to"]) for e in card["joins"]}
    assert edges == {
        ("customer.c_nationkey", "nation.n_nationkey"),
        ("nation.n_regionkey", "region.r_regionkey"),
        ("orders.o_custkey", "customer.c_custkey"),
    }
    assert all(e["source"] == "inferred" for e in card["joins"])


def test_notes_are_annotations_not_exclusions(card):
    cols = column_index(card)
    assert NOTE_CODED in cols["customer.c_flag"]["notes"]
    assert NOTE_CONSTANT in cols["customer.c_const"]["notes"]
    # every column still counts toward coverage
    assert card["eligible"] == {"tables": 4, "columns": 17}


def test_schema_card_markdown_warns_about_coded_columns_without_docs(card):
    assert "NO DOCS SUPPLIED" in render_schema_card_md(card, docs_supplied=False)
    assert "NO DOCS SUPPLIED" not in render_schema_card_md(card, docs_supplied=True)
