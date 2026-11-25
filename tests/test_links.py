import datetime as dt

from t2s_eval.joins import connect_tables
from t2s_eval.links import Link, LinkChecker, label_check, parse_date_spec, phrase_in_question

Q = "Which customers in Europe placed orders worth more than 200 in 1996?"


def L(**kw):
    return Link(**kw)


def test_phrase_matching():
    assert phrase_in_question("customers in EUROPE", Q)
    assert phrase_in_question("customers … in 1996", Q)
    assert phrase_in_question("customers ... 1996", Q)
    assert not phrase_in_question("1996 … customers", Q)  # parts must appear in order
    assert not phrase_in_question("suppliers", Q)
    assert not phrase_in_question("", Q)


def test_date_specs():
    assert parse_date_spec("1997") == (dt.date(1997, 1, 1), dt.date(1997, 12, 31))
    assert parse_date_spec("1997-02") == (dt.date(1997, 2, 1), dt.date(1997, 2, 28))
    assert parse_date_spec("1997-Q4") == (dt.date(1997, 10, 1), dt.date(1997, 12, 31))
    assert parse_date_spec("1993..1997") == (dt.date(1993, 1, 1), dt.date(1997, 12, 31))
    assert parse_date_spec("1995-03-15") == (dt.date(1995, 3, 15), dt.date(1995, 3, 15))


def test_column_and_value_checks(checker):
    ok = checker.check_link(L(phrase="Europe", kind="column", columns=["region.r_name"], value="EUROPE"), Q)
    assert ok.ok
    bad_col = checker.check_link(L(phrase="customers", kind="column", columns=["customer.c_age"]), Q)
    assert not bad_col.ok and "does not exist" in bad_col.problems[0]
    bad_val = checker.check_link(L(phrase="Europe", kind="column", columns=["region.r_name"], value="ASIA"), Q)
    assert not bad_val.ok
    old = checker.check_link(L(phrase="in 1996", kind="column", columns=["orders.o_orderdate"], value="1990"), Q)
    assert not old.ok and "outside" in old.problems[0]
    in_range = checker.check_link(L(phrase="more than 200", kind="column", columns=["orders.o_totalprice"], value="200"), Q)
    assert in_range.ok
    too_big = checker.check_link(L(phrase="more than 200", kind="column", columns=["orders.o_totalprice"], value="99999"), Q)
    assert not too_big.ok
    no_table = checker.check_link(L(phrase="customers", kind="column", columns=["c_name"]), Q)
    assert not no_table.ok and "table.column" in no_table.problems[0]


def test_shape_checks(checker):
    assert not checker.check_link(L(phrase="Which", kind="shape", shape="pivot"), Q).ok
    derived = checker.check_link(L(phrase="customers", kind="shape", shape="multi_join"), Q)
    assert derived.ok and derived.ignored


def test_analyze_derives_join_shape_and_credits_linked_items_only(checker):
    links = [
        L(phrase="customers", kind="table", table="customer"),
        L(phrase="Europe", kind="column", columns=["region.r_name"], value="EUROPE"),
        L(phrase="in 1996", kind="column", columns=["orders.o_orderdate"], value="1996"),
        L(phrase="Which", kind="shape", shape="lookup"),
    ]
    a = checker.analyze(Q, links)
    assert a.all_links_ok and a.connected
    assert a.path_tables == ["customer", "nation", "orders", "region"]
    assert a.tables == {"customer", "region", "orders"}  # nation is only on the path: no credit
    assert a.columns == {"region.r_name", "orders.o_orderdate"}  # no join keys
    assert a.shapes == {"lookup", "multi_join"}


def test_missing_and_ambiguous_links(checker):
    q = "What is the average age and the delay of customers?"
    links = [
        L(phrase="age", kind="missing", concept="customer age", closest=["customer.c_acctbal"], why_not="no age column"),
        L(phrase="delay", kind="column", columns=["orders.o_orderdate"], alternatives=[["customer.c_acctbal"]]),
    ]
    a = checker.analyze(q, links)
    assert a.missing[0]["concept"] == "customer age"
    assert a.ambiguous and not a.columns


def test_disconnected_tables(card, mini_db, legend):
    card = {**card, "joins": []}
    a = LinkChecker(card, mini_db, legend).analyze(Q, [
        L(phrase="customers", kind="table", table="customer"),
        L(phrase="Europe", kind="column", columns=["region.r_name"], value="EUROPE"),
    ])
    assert not a.connected


def test_connect_tables_basic():
    adj = {"a": {"b"}, "b": {"a", "c"}, "c": {"b"}, "d": set()}
    assert connect_tables({"a", "c"}, adj) == (True, ["a", "b", "c"])
    assert connect_tables({"a"}, adj) == (True, ["a"])
    assert connect_tables({"a", "d"}, adj)[0] is False


def test_label_check(checker):
    a = checker.analyze(Q, [L(phrase="customers", kind="table", table="customer")])
    out = label_check({"tables": ["customer", "orders"], "shapes": []}, a)
    status = {(x["dimension"], x["item"]): x["status"] for x in out}
    assert status[("tables", "customer")] == "confirmed"
    assert status[("tables", "orders")] == "not supported"
    assert label_check(None, a) == []
