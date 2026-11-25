from t2s_eval.anchor import render_anchor_md, resolve_anchor


def test_fixed_anchor_ranges():
    a = resolve_anchor("1998-08-02", "orders.o_orderdate", None)
    r = a["ranges"]
    assert a["date"] == "1998-08-02" and a["mode"] == "fixed"
    assert (r["last quarter"]["from"], r["last quarter"]["to"], r["last quarter"]["value"]) == ("1998-04-01", "1998-06-30", "1998-Q2")
    assert r["this quarter"]["value"] == "1998-Q3"
    assert (r["last year"]["from"], r["last year"]["to"]) == ("1997-01-01", "1997-12-31")
    assert r["last month"]["value"] == "1998-07"
    assert r["last 12 months"]["value"] == "1997-08-03..1998-08-02"
    assert r["this year"]["value"] == "1998"


def test_quarter_boundaries_in_january():
    r = resolve_anchor("1996-01-10", "x.y", None)["ranges"]
    assert r["last quarter"]["value"] == "1995-Q4"
    assert (r["last quarter"]["from"], r["last quarter"]["to"]) == ("1995-10-01", "1995-12-31")
    assert r["last month"]["value"] == "1995-12"


def test_auto_anchor_uses_latest_value(mini_db):
    a = resolve_anchor("auto", "orders.o_orderdate", mini_db)
    assert a["mode"] == "auto" and a["date"] == "1998-08-02"


def test_off():
    a = resolve_anchor("off", "orders.o_orderdate", None)
    assert a["mode"] == "off" and a["date"] is None and a["ranges"] == {}
    assert "OFF" in render_anchor_md(a)
    assert resolve_anchor("auto", None, None)["mode"] == "off"
