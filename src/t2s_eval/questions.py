"""The question file: the judges' only input besides the database and docs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_FIELDS = {"id", "text", "labels"}
LABEL_DIMS = ("tables", "columns", "shapes")


class QuestionFileError(ValueError):
    pass


def load_questions(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate and clean a question file. Returns (questions, warnings).

    Only id, text and labels are kept; any other field is dropped with a warning, so an
    edited file can never pass hidden inputs to a judge.
    """
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise QuestionFileError(f"{path}: not valid JSON ({e})") from e
    items = data.get("questions") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        raise QuestionFileError(f"{path}: expected an object with a non-empty 'questions' list")
    warnings: list[str] = []
    if isinstance(data, dict):
        extra_top = sorted(set(data) - {"questions"})
        if extra_top:
            warnings.append(f"top-level fields ignored: {', '.join(extra_top)}")
    seen: set[str] = set()
    out = []
    for i, q in enumerate(items, 1):
        if not isinstance(q, dict):
            raise QuestionFileError(f"question #{i}: expected an object")
        qid = str(q.get("id", "")).strip()
        text = str(q.get("text", "")).strip()
        if not qid:
            raise QuestionFileError(f"question #{i}: missing id")
        if qid in seen:
            raise QuestionFileError(f"duplicate id: {qid}")
        if not text:
            raise QuestionFileError(f"{qid}: empty text")
        seen.add(qid)
        extra = sorted(set(q) - ALLOWED_FIELDS)
        if extra:
            warnings.append(f"{qid}: fields ignored: {', '.join(extra)}")
        clean: dict[str, Any] = {"id": qid, "text": text}
        labels = q.get("labels")
        if isinstance(labels, dict):
            clean["labels"] = {d: [str(x) for x in labels.get(d, [])] for d in LABEL_DIMS if d in labels}
        elif labels is not None:
            warnings.append(f"{qid}: labels ignored (not an object)")
        out.append(clean)
    return out, warnings


def judge_view(questions: list[dict[str, Any]]) -> list[dict[str, str]]:
    """What the judge LLM sees: ids and texts only. Labels are checked by code, never shown."""
    return [{"id": q["id"], "text": q["text"]} for q in questions]
