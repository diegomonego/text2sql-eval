"""The skills' code steps end to end, with hand-written stand-ins for the LLM's output."""

import json

from t2s_eval import generator, judges
from t2s_eval.check_run import check_run

CANDIDATES = [
    {"target": "t01", "question": "Which customers in Europe placed orders in 1996?", "links": [
        {"phrase": "customers", "kind": "table", "table": "customer"},
        {"phrase": "Europe", "kind": "column", "columns": ["region.r_name"], "value": "EUROPE"},
        {"phrase": "in 1996", "kind": "column", "columns": ["orders.o_orderdate"], "value": "1996"},
        {"phrase": "Which", "kind": "shape", "shape": "lookup"}]},
    {"target": "t02", "question": "What is the total order value per market segment?", "links": [
        {"phrase": "total", "kind": "shape", "shape": "aggregation"},
        {"phrase": "order value", "kind": "column", "columns": ["orders.o_totalprice"]},
        {"phrase": "market segment", "kind": "column", "columns": ["customer.c_mktsegment"]}]},
    {"target": "t03", "question": "Which customers have never placed an order?", "links": [
        {"phrase": "customers", "kind": "column", "columns": ["customer.c_name"]},
        {"phrase": "never", "kind": "shape", "shape": "anti_join"},
        {"phrase": "placed an order", "kind": "table", "table": "orders"}]},
    # same computation as the second one, different wording -> duplicate
    {"target": "t04", "question": "For each market segment, what is the total value of orders?", "links": [
        {"phrase": "total", "kind": "shape", "shape": "aggregation"},
        {"phrase": "value of orders", "kind": "column", "columns": ["orders.o_totalprice"]},
        {"phrase": "market segment", "kind": "column", "columns": ["customer.c_mktsegment"]}]},
    # dropped: raw column name
    {"target": "t05", "question": "What is the sum of o_totalprice?", "links": [
        {"phrase": "sum", "kind": "shape", "shape": "aggregation"},
        {"phrase": "o_totalprice", "kind": "column", "columns": ["orders.o_totalprice"]}]},
    # dropped: concept not in the database
    {"target": "t06", "question": "What is the average customer age?", "links": [
        {"phrase": "average", "kind": "shape", "shape": "aggregation"},
        {"phrase": "customer age", "kind": "missing", "concept": "age"}]},
    # dropped: value not in the data
    {"target": "f01", "question": "How many customers are in Asia?", "links": [
        {"phrase": "How many", "kind": "shape", "shape": "aggregation"},
        {"phrase": "Asia", "kind": "column", "columns": ["region.r_name"], "value": "ASIA"}]},
]


def test_generator_selects_exactly_n_and_records_why(project, tmp_path):
    out = tmp_path / "run"
    msg = generator.prepare(project, 2, out, no_docs=False, anchor_setting=None)
    assert "brief.md" in msg
    brief = (out / "generation" / "brief.md").read_text()
    assert "1998-08-02" in brief and "glossary.md" in brief and "`multi_join`" in brief
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": CANDIDATES}))
    code, msg = generator.select(project, out)
    assert code == 0, msg
    qs = json.loads((out / "questions.json").read_text())["questions"]
    assert [q["id"] for q in qs] == ["q01", "q02"]
    pool = {c["id"]: c for c in json.loads((out / "generation" / "pool.json").read_text())["candidates"]}
    assert pool["c004"]["status"] == "duplicate" and pool["c004"]["duplicate_of"] == "c002"
    assert "raw column name" in pool["c005"]["reason"]
    assert "not in the database" in pool["c006"]["reason"]
    assert "ASIA" in pool["c007"]["reason"]
    assert sum(c["status"] == "selected" for c in pool.values()) == 2
    run = json.loads((out / "generation" / "run.json").read_text())
    assert run["input"]["n"] == 2 and run["config"]["time_anchor"]["date"] == "1998-08-02"
    # the first pick is the multi-table lookup (3 tables + 2 shapes), labels come from its links
    assert set(qs[0]["labels"]["shapes"]) == {"lookup", "multi_join"}


def test_generator_asks_for_more_candidates_when_short(project, tmp_path):
    out = tmp_path / "run"
    generator.prepare(project, 4, out, no_docs=False, anchor_setting=None)
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": CANDIDATES}))
    code, msg = generator.select(project, out)
    assert code == 4 and "candidates_round2.json" in msg
    assert not (out / "questions.json").exists()


def test_generator_without_docs_drops_coded_columns(project, tmp_path):
    out = tmp_path / "run"
    generator.prepare(project, 1, out, no_docs=True, anchor_setting="off")
    assert "No docs supplied" in (out / "generation" / "brief.md").read_text()
    cand = {"target": "t01", "question": "How many customers have flag A?", "links": [
        {"phrase": "How many", "kind": "shape", "shape": "aggregation"},
        {"phrase": "flag A", "kind": "column", "columns": ["customer.c_flag"], "value": "A"}]}
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": [cand, CANDIDATES[1]]}))
    code, msg = generator.select(project, out)
    assert code == 0
    pool = json.loads((out / "generation" / "pool.json").read_text())["candidates"]
    assert "coded column without docs" in pool[0]["reason"]


def test_judges_finalize_and_run_check(project, tmp_path):
    out = tmp_path / "run"
    generator.prepare(project, 2, out, no_docs=False, anchor_setting=None)
    (out / "generation" / "candidates.json").write_text(json.dumps({"candidates": CANDIDATES}))
    assert generator.select(project, out)[0] == 0
    qfile = out / "questions.json"
    qs = json.loads(qfile.read_text())["questions"]
    links = {c["question"]: c["links"] for c in CANDIDATES}

    judges.prepare(project, "correctness", qfile, out, no_docs=False, anchor_setting=None)
    seen = json.loads((out / "work" / "correctness" / "questions_for_judge.json").read_text())
    assert all(set(q) == {"id", "text"} for q in seen["questions"])  # no labels for the LLM
    raw = {"results": [{"id": q["id"], "verdict": "ANSWERABLE", "rationale": "ok", "links": links[q["text"]]} for q in qs]}
    (out / "work" / "correctness" / "raw.json").write_text(json.dumps(raw))
    code, msg = judges.finalize(project, "correctness", qfile, out, accept_issues=False)
    assert code == 0, msg
    rep = json.loads((out / "correctness.json").read_text())
    assert rep["summary"]["score"] == 1.0 and (out / "correctness.md").exists()

    judges.prepare(project, "coverage", qfile, out, no_docs=False, anchor_setting=None)
    (out / "work" / "coverage" / "raw.json").write_text(json.dumps({"results": [{"id": q["id"], "links": links[q["text"]]} for q in qs]}))
    code, msg = judges.finalize(project, "coverage", qfile, out, accept_issues=False)
    assert code == 0, msg
    md = (out / "coverage.md").read_text()
    assert md.startswith("# Coverage report")
    # dimensions and uncovered items come first, the summary score last
    assert md.index("## Coverage by dimension") < md.index("## Repetition") < md.index("## Summary score")
    assert "**Uncovered columns (" in md and "mostly tracks column coverage" in md

    code, msg = check_run(out)
    assert code == 0, msg
    assert "no run log" in msg  # no claude -p logs in this test
    assert "claimed vs verified columns: generator" in msg
    # a run log showing a different model than the metadata is a mismatch
    (out / "logs").mkdir()
    (out / "logs" / "correctness.json").write_text(json.dumps({"modelUsage": {
        "claude-haiku-5-5": {"costUSD": 0.0001}, "claude-sonnet-5-5": {"costUSD": 0.3}}}))
    code, msg = check_run(out)
    assert code == 1 and "run log shows claude-sonnet-5-5" in msg
    (out / "logs" / "correctness.json").write_text(json.dumps({"modelUsage": {
        "claude-haiku-5-5": {"costUSD": 0.0001}, project.models["correctness_judge"]: {"costUSD": 0.3}}}))
    assert check_run(out)[0] == 0
    # editing the question file after judging is detected
    qfile.write_text(qfile.read_text().replace("Europe", "Africa"))
    assert check_run(out)[0] == 1


def test_judge_finalize_rejects_bad_format_and_missing_ids(project, tmp_path):
    out = tmp_path / "run"
    qfile = tmp_path / "q.json"
    qfile.write_text(json.dumps({"questions": [{"id": "a", "text": "How many orders?"}, {"id": "b", "text": "Which region?"}]}))
    judges.prepare(project, "correctness", qfile, out, no_docs=False, anchor_setting=None)
    (out / "work" / "correctness" / "raw.json").write_text(json.dumps({"results": [{"id": "a", "verdict": "MAYBE"}]}))
    code, msg = judges.finalize(project, "correctness", qfile, out, accept_issues=False)
    assert code == 2 and "verdict" in msg and "no result for: a, b" in msg
