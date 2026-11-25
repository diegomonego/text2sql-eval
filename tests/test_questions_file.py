import json

import pytest

from t2s_eval.questions import QuestionFileError, judge_view, load_questions


def write(tmp_path, data):
    p = tmp_path / "q.json"
    p.write_text(json.dumps(data) if not isinstance(data, str) else data)
    return p


def test_unknown_fields_are_dropped_with_warnings(tmp_path):
    p = write(tmp_path, {"meta": {"x": 1}, "questions": [
        {"id": "q1", "text": "How many orders?", "labels": {"tables": ["orders"]}, "notes": "reviewer note"},
    ]})
    qs, warnings = load_questions(p)
    assert qs == [{"id": "q1", "text": "How many orders?", "labels": {"tables": ["orders"]}}]
    assert any("meta" in w for w in warnings) and any("notes" in w for w in warnings)


def test_judges_never_see_labels(tmp_path):
    qs, _ = load_questions(write(tmp_path, {"questions": [{"id": "q1", "text": "x?", "labels": {"shapes": ["ranking"]}}]}))
    assert judge_view(qs) == [{"id": "q1", "text": "x?"}]


@pytest.mark.parametrize("data,msg", [
    ({"questions": [{"id": "q1", "text": "a"}, {"id": "q1", "text": "b"}]}, "duplicate id"),
    ({"questions": [{"id": "q1", "text": "  "}]}, "empty text"),
    ({"questions": [{"text": "a"}]}, "missing id"),
    ({"questions": []}, "non-empty"),
    ("{not json", "not valid JSON"),
])
def test_invalid_files(tmp_path, data, msg):
    with pytest.raises(QuestionFileError, match=msg):
        load_questions(write(tmp_path, data))
