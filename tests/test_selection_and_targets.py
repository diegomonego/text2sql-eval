import pytest

from t2s_eval.config import PoolSettings
from t2s_eval.selection import GainSettings, NotEnoughCandidates, Scored, dedupe, gain_parts, greedy_select
from t2s_eval.targets import build_targets, pool_sizes

G = GainSettings(weights={"a": 1.0, "b": 0.5}, repeat_penalty=0.5, lambda_shape=0.5, lambda_table=0.25,
                 lambda_column=0.25, n_tables=4, n_columns=10)


def S(cid, shapes, tables, cols):
    return Scored(cid, frozenset(tables), frozenset(cols), frozenset(shapes))


A = S("A", {"a"}, {"t1"}, {"c1"})
B = S("B", {"a", "b"}, {"t1", "t2"}, {"c1", "c2"})
C = S("C", {"b"}, {"t3"}, {"c3", "c4", "c5"})


def test_gain_matches_hand_calculation():
    # B: 0.5 * 1.5/1.5 + 0.25 * 2/4 + 0.25 * 2/10
    assert gain_parts(B, {}, set(), set(), G)["total"] == pytest.approx(0.675)
    # A after B: shape a repeated (worth 0.5), table and column already covered
    assert gain_parts(A, {"a": 1, "b": 1}, {"t1", "t2"}, {"c1", "c2"}, G)["total"] == pytest.approx(0.5 * 0.5 / 1.5)


def test_greedy_picks_by_marginal_gain():
    picks, log = greedy_select([A, B, C], 2, G)
    assert [p.id for p in picks] == ["B", "C"]  # C beats A once B covered t1, c1 and shape a
    assert log[1]["gain"]["total"] == pytest.approx(0.5 * 0.25 / 1.5 + 0.25 / 4 + 0.25 * 3 / 10, abs=1e-6)


def test_exactly_n_and_not_enough():
    assert len(greedy_select([A, B, C], 3, G)[0]) == 3
    with pytest.raises(NotEnoughCandidates):
        greedy_select([A, B], 3, G)


def test_ties_go_to_the_earliest_candidate():
    x, y = S("x", {"a"}, {"t1"}, set()), S("y", {"a"}, {"t1"}, set())
    assert greedy_select([x, y], 1, G)[0][0].id == "x"


def test_gains_never_increase_between_rounds():
    cands = [A, B, C, S("D", {"b"}, {"t4"}, {"c6"}), S("E", {"a"}, {"t2", "t3"}, {"c7"})]
    _, log = greedy_select(cands, 5, G)
    last: dict[str, float] = {}
    for rnd in log:
        for c in rnd["candidates"]:
            assert c["total"] <= last.get(c["id"], 1e9) + 1e-9
            last[c["id"]] = c["total"]


def test_dedupe_ignores_filter_values_and_keeps_first():
    b2 = S("B2", {"a", "b"}, {"t1", "t2"}, {"c1", "c2"})  # same computation, different wording/values
    unique, dups = dedupe([B, A, b2])
    assert [u.id for u in unique] == ["B", "A"] and dups == {"B2": "B"}


def test_pool_sizes():
    pool = PoolSettings()
    assert pool_sizes(1, pool) == (16, 1)
    assert pool_sizes(5, pool) == (16, 5)
    assert pool_sizes(15, pool) == (30, 15)


def test_targets_cover_every_shape_and_table():
    shapes = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
    card = {"tables": [{"name": f"t{i}", "rows": 100 - i} for i in range(8)]}
    targets = build_targets(5, shapes, card, PoolSettings())
    targeted = [t for t in targets if t["kind"] == "targeted"]
    assert len(targeted) == 16 and len([t for t in targets if t["kind"] == "free"]) == 5
    assert all(sum(t["shape"] == s for t in targeted) >= 2 for s in shapes)
    assert {t["focus_table"] for t in targeted} == {f"t{i}" for i in range(8)}
    pairs = [(t["shape"], t["focus_table"]) for t in targeted]
    assert len(pairs) == len(set(pairs))
    with pytest.raises(ValueError):
        build_targets(0, shapes, card, PoolSettings())
