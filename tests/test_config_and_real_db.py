"""Config consistency, and checks against the real TPC-H database when it has been built."""

import re
import shutil

import pytest

from t2s_eval.config import load_config
from t2s_eval.legend import load_legend
from t2s_eval.skills import SKILL_FOR_COMPONENT, read_model, skill_path, sync_skills

from .conftest import ROOT


def test_every_skill_pins_its_configured_model():
    cfg = load_config(ROOT)
    for component, skill in SKILL_FOR_COMPONENT.items():
        text = (ROOT / ".claude" / "skills" / skill / "SKILL.md").read_text()
        m = re.search(r"^model:\s*(\S+)\s*$", text, re.M)
        assert m and m.group(1) == cfg.models[component], f"{skill} drifted from config/eval.toml: run `make skills`"


def test_sync_copies_each_model_from_config_into_its_skill(tmp_path):
    root = tmp_path / "proj"
    shutil.copytree(ROOT / "config", root / "config")
    shutil.copytree(ROOT / ".claude" / "skills", root / ".claude" / "skills")
    toml = (root / "config" / "eval.toml").read_text()
    toml = toml.replace('correctness_judge = "claude-opus-5-5"', 'correctness_judge = "claude-fable-5-2"')
    toml = toml.replace('coverage_judge = "claude-opus-5-5"', 'coverage_judge = "claude-sonnet-5-5"')
    (root / "config" / "eval.toml").write_text(toml)
    cfg = load_config(root)
    assert cfg.models == {"generator": "claude-opus-5-5", "correctness_judge": "claude-fable-5-2",
                          "coverage_judge": "claude-sonnet-5-5"}
    in_sync, lines = sync_skills(cfg, check=True)
    assert not in_sync and any("judge-correctness" in l and "claude-fable-5-2" in l for l in lines)
    assert read_model(skill_path(root, "correctness_judge")) == "claude-opus-5-5"  # check mode writes nothing
    sync_skills(cfg)
    assert read_model(skill_path(root, "correctness_judge")) == "claude-fable-5-2"
    assert read_model(skill_path(root, "coverage_judge")) == "claude-sonnet-5-5"
    assert read_model(skill_path(root, "generator")) == "claude-opus-5-5"
    assert sync_skills(cfg, check=True)[0]
    # the rest of the skill file is untouched
    body = skill_path(root, "coverage_judge").read_text()
    assert body.replace("claude-sonnet-5-5", "claude-opus-5-5") == (ROOT / ".claude/skills/judge-coverage/SKILL.md").read_text()


def test_one_model_for_all_components_and_missing_models(tmp_path):
    root = tmp_path / "proj"
    shutil.copytree(ROOT / "config", root / "config")
    toml = (root / "config" / "eval.toml").read_text()
    start = toml.index("[model]")
    end = toml.index("[spec]")
    (root / "config" / "eval.toml").write_text(toml[:start] + '[model]\nid = "claude-sonnet-5-5"\n\n' + toml[end:])
    assert set(load_config(root).models.values()) == {"claude-sonnet-5-5"}
    (root / "config" / "eval.toml").write_text(toml[:start] + '[model]\ngenerator = "claude-opus-5-5"\n\n' + toml[end:])
    with pytest.raises(ValueError, match="correctness_judge"):
        load_config(root)


def test_config_file_can_be_switched_with_an_environment_variable(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    shutil.copytree(ROOT / "config", root / "config")
    alt = (root / "config" / "eval.toml").read_text().replace("data/tpch_sf01.duckdb", "data/other.duckdb")
    (root / "config" / "alt.toml").write_text(alt)
    assert load_config(root).db_url.endswith("tpch_sf01.duckdb")
    monkeypatch.setenv("T2S_CONFIG", "config/alt.toml")
    cfg = load_config(root)
    assert cfg.db_url.endswith("other.duckdb") and cfg.config_path == root / "config" / "alt.toml"
    monkeypatch.setenv("T2S_CONFIG", "config/missing.toml")
    with pytest.raises(FileNotFoundError, match="T2S_CONFIG"):
        load_config(root)


def test_legend_weights():
    lg = load_legend(ROOT / "config" / "shapes.toml")
    assert len(lg.shapes) == 8 and lg.derived_ids == {"multi_join"}
    w = lg.weights
    # I calibrated from BIRD Mini-Dev (calibration/bird_i.py); W = (0.4 F + 0.6 I) / 3
    assert w["lookup"] == pytest.approx(0.6)
    assert w["aggregation"] == pytest.approx((0.4 * 3 + 0.6 * 1.7) / 3)
    assert w["ranking"] == pytest.approx((0.4 * 3 + 0.6 * 1.3) / 3)
    assert w["multi_join"] == pytest.approx((0.4 * 2 + 0.6 * 2.8) / 3)
    assert w["anti_join"] == pytest.approx(2.2 / 3)
    assert lg.sum_weights == pytest.approx(6.0267, abs=1e-3)


def test_legend_rejects_scores_outside_1_to_3(tmp_path):
    text = (ROOT / "config" / "shapes.toml").read_text().replace("I = 1.3", "I = 4", 1)
    (tmp_path / "shapes.toml").write_text(text)
    with pytest.raises(ValueError, match="ranking: I must be between 1 and 3"):
        load_legend(tmp_path / "shapes.toml")


REAL_DB = ROOT / "data" / "tpch_sf01.duckdb"


@pytest.mark.skipif(not REAL_DB.exists(), reason="TPC-H database not built (run `make db`)")
def test_real_tpch_schema_card():
    from t2s_eval.anchor import resolve_anchor
    from t2s_eval.db import connect
    from t2s_eval.schema_card import NOTE_CODED, NOTE_CONSTANT, build_schema_card, column_index

    cfg = load_config(ROOT)
    db = connect(cfg.db_url, cfg.root)
    card = build_schema_card(db, cfg.max_listed_values)
    assert card["eligible"] == {"tables": 8, "columns": 61}
    edges = {(e["from"].split(".")[0], e["to"].split(".")[0]) for e in card["joins"]}
    assert edges == {
        ("customer", "nation"), ("lineitem", "orders"), ("lineitem", "part"), ("lineitem", "supplier"),
        ("nation", "region"), ("orders", "customer"), ("partsupp", "part"), ("partsupp", "supplier"),
        ("supplier", "nation"),
    }
    cols = column_index(card)
    assert {c for c, i in cols.items() if NOTE_CODED in i["notes"]} == {
        "lineitem.l_returnflag", "lineitem.l_linestatus", "orders.o_orderstatus"}
    assert {c for c, i in cols.items() if NOTE_CONSTANT in i["notes"]} == {"orders.o_shippriority"}
    assert resolve_anchor("auto", cfg.anchor_column, db)["date"] == "1998-08-02"
    db.close()
