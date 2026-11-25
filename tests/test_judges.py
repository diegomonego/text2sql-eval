import json

import pytest

from t2s_eval.judges import CorrectnessItem, CoverageItem, evaluate_correctness, evaluate_coverage

QUESTIONS = [
    {"id": "q1", "text": "Which customers in Europe placed orders in 1996?", "labels": {"tables": ["customer", "orders"]}},
    {"id": "q2", "text": "What is the average age of our customers?"},
    {"id": "q3", "text": "What was the delay for urgent orders?"},
    {"id": "q4", "text": "What is the capital of Australia?"},
]

Q1_LINKS = [
    {"phrase": "customers", "kind": "table", "table": "customer"},
    {"phrase": "Europe", "kind": "column", "columns": ["region.r_name"], "value": "EUROPE"},
    {"phrase": "in 1996", "kind": "column", "columns": ["orders.o_orderdate"], "value": "1996"},
    {"phrase": "Which", "kind": "shape", "shape": "lookup"},
]
Q2_LINKS = [
    {"phrase": "average", "kind": "shape", "shape": "aggregation"},
    {"phrase": "age", "kind": "missing", "concept": "customer age", "closest": ["customer.c_acctbal"], "why_not": "no age data"},
]
Q3_LINKS = [
    {"phrase": "urgent orders", "kind": "column", "columns": ["orders.o_orderpriority"], "value": "1-URGENT"},
    {"phrase": "delay", "kind": "column", "columns": ["orders.o_orderdate"], "alternatives": [["orders.o_totalprice"]]},
]


def correctness_items(q1_verdict="ANSWERABLE"):
    return [CorrectnessItem.model_validate(x) for x in [
        {"id": "q1", "verdict": q1_verdict, "rationale": "All concepts exist.", "links": Q1_LINKS},
        {"id": "q2", "verdict": "MISSING_DATA", "rationale": "No age column.", "links": Q2_LINKS},
        {"id": "q3", "verdict": "AMBIGUOUS", "rationale": "Delay is undefined.", "links": Q3_LINKS},
        {"id": "q4", "verdict": "OFF_TOPIC", "rationale": "Geography trivia."},
    ]]


def test_correctness_score_and_counts(checker):
    results, summary, issues = evaluate_correctness(QUESTIONS, correctness_items(), checker)
    assert issues == []
    assert summary["counts"] == {"OFF_TOPIC": 1, "MISSING_DATA": 1, "AMBIGUOUS": 1, "ANSWERABLE": 1}
    assert summary["score"] == pytest.approx((1 + 0.5 * 1) / 4)
    assert "(1 + 0.5 x 1) / 4" in summary["calculation"]
    q1 = results[0]
    assert {x["status"] for x in q1["label_check"] if x["dimension"] == "tables"} == {"confirmed", "not labeled"}


def test_correctness_flags_verdicts_without_evidence(checker):
    items = correctness_items()
    items[1] = CorrectnessItem.model_validate({"id": "q2", "verdict": "ANSWERABLE", "rationale": "x", "links": Q2_LINKS})
    items[0] = CorrectnessItem.model_validate({"id": "q1", "verdict": "MISSING_DATA", "rationale": "x", "links": Q1_LINKS})
    results, summary, issues = evaluate_correctness(QUESTIONS, items, checker)
    assert any("q2: ANSWERABLE but a concept is marked missing" in i for i in issues)
    assert any("q1: MISSING_DATA needs" in i for i in issues)
    assert summary["verdicts_with_evidence_issues"] == 2


def coverage_items(extra_q5=None):
    items = [
        {"id": "q1", "links": Q1_LINKS},
        {"id": "q2", "links": Q2_LINKS},
        {"id": "q3", "links": Q3_LINKS},
        {"id": "q4", "links": []},
    ]
    return [CoverageItem.model_validate(x) for x in items]


def test_coverage_credit_rules(checker, card, legend):
    report, issues = evaluate_coverage(QUESTIONS, coverage_items(), checker, card, legend.ids, docs_supplied=True)
    pq = {p["id"]: p for p in report["per_question"]}
    assert pq["q1"]["credited"]["tables"] == ["customer", "orders", "region"]
    assert pq["q1"]["credited"]["shapes"] == ["lookup", "multi_join"]
    # q2 has a concept the database lacks: no credit at all, not even for its aggregation shape
    assert not pq["q2"]["supported"] and pq["q2"]["credited"] == {"tables": [], "columns": [], "shapes": []}
    # q3: the ambiguous phrase earns nothing, the rest still counts
    assert pq["q3"]["credited"]["columns"] == ["orders.o_orderpriority"]
    assert any(x["reason"].startswith("ambiguous") for x in pq["q3"]["not_credited"])
    dims = report["dimensions"]
    assert dims["tables"]["covered_count"] == 3 and dims["tables"]["eligible"] == 4
    assert dims["columns"]["eligible"] == 17
    assert report["repetition"]["no_credit"] == ["q2"]
    s = report["summary"]
    assert s["score"] == pytest.approx((dims["tables"]["pct"] + dims["columns"]["pct"] + dims["shapes"]["pct"]) / 3, abs=0.01)
    assert dims["columns"]["uncovered"]["customer.c_const"] == "not asked (constant in this data)"
    assert issues == []


def test_coverage_without_docs_marks_coded_columns(checker, card, legend):
    report, _ = evaluate_coverage(QUESTIONS, coverage_items(), checker, card, legend.ids, docs_supplied=False)
    assert report["dimensions"]["columns"]["uncovered"]["customer.c_flag"] == "not coverable without docs (coded values)"


def test_paraphrase_twins_are_duplicates_and_cover_nothing_unique(checker, card, legend):
    qs = QUESTIONS[:1] + [{"id": "q5", "text": "List customers in Europe who placed orders in 1996."}]
    items = [CoverageItem.model_validate({"id": "q1", "links": Q1_LINKS}),
             CoverageItem.model_validate({"id": "q5", "links": [
                 {"phrase": "customers", "kind": "table", "table": "customer"},
                 {"phrase": "Europe", "kind": "column", "columns": ["region.r_name"], "value": "EUROPE"},
                 {"phrase": "in 1996", "kind": "column", "columns": ["orders.o_orderdate"], "value": "1996"},
                 {"phrase": "List", "kind": "shape", "shape": "lookup"}]})]
    report, _ = evaluate_coverage(qs, items, checker, card, legend.ids, docs_supplied=True)
    assert report["repetition"]["duplicate_pairs"] == [["q1", "q5"]]
    assert report["repetition"]["nothing_unique"] == ["q1", "q5"]


def test_coverage_reports_failed_links_as_issues(checker, card, legend):
    items = coverage_items()
    items[0] = CoverageItem.model_validate({"id": "q1", "links": Q1_LINKS + [
        {"phrase": "customers", "kind": "column", "columns": ["customer.c_age"]}]})
    report, issues = evaluate_coverage(QUESTIONS, items, checker, card, legend.ids, docs_supplied=True)
    assert any("c_age" in i for i in issues)
    assert "customer.c_age" not in report["dimensions"]["columns"]["covered"]


def test_judges_take_db_and_docs_as_arguments(project, tmp_path, mini_db_path):
    """judge-prepare records --db/--docs; judge-finalize reuses them even if the config's database is unusable."""
    from dataclasses import replace

    from t2s_eval import judges as J

    cfg = replace(project, db_url="duckdb:///does/not/exist.duckdb")
    docs = tmp_path / "judge_docs"
    docs.mkdir()
    (docs / "terms.md").write_text("# Terms\n\nOrder value = o_totalprice.\n")
    qfile = tmp_path / "q.json"
    qfile.write_text(json.dumps({"questions": [{"id": "a", "text": "What is the total order value per market segment?"}]}))
    out = tmp_path / "run"
    J.prepare(cfg, "coverage", qfile, out, no_docs=False, anchor_setting=None, db_url=f"duckdb:///{mini_db_path}", docs=str(docs))
    settings = json.loads((out / "work" / "coverage" / "settings.json").read_text())
    assert settings["db_url"] == f"duckdb:///{mini_db_path}" and settings["docs_dir"] == str(docs)
    raw = {"results": [{"id": "a", "links": [
        {"phrase": "total", "kind": "shape", "shape": "aggregation"},
        {"phrase": "order value", "kind": "column", "columns": ["orders.o_totalprice"]},
        {"phrase": "market segment", "kind": "column", "columns": ["customer.c_mktsegment"]}]}]}
    (out / "work" / "coverage" / "raw.json").write_text(json.dumps(raw))
    code, msg = J.finalize(cfg, "coverage", qfile, out, accept_issues=False)
    assert code == 0, msg
    report = json.loads((out / "coverage.json").read_text())
    assert report["meta"]["docs"][0]["path"] == str(docs / "terms.md")
