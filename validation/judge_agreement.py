"""Agreement between the correctness judge and a labeled question set.

Usage:
    python3 validation/judge_agreement.py runs/labeled_20

Reads <run>/labels.json (expected verdicts) and <run>/correctness.json (the judge's report) and prints
raw agreement, Cohen's kappa, the confusion matrix, and every disagreement with both rationales.
Writes <run>/agreement.json. No dependencies beyond the standard library.

Cohen's kappa = (p_o - p_e) / (1 - p_e), where p_o is the observed agreement and p_e the agreement
expected by chance from each side's verdict frequencies.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

VERDICTS = ["OFF_TOPIC", "MISSING_DATA", "AMBIGUOUS", "ANSWERABLE"]


def kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    p_o = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    p_e = sum(ca[v] * cb[v] for v in VERDICTS) / (n * n)
    return 1.0 if p_e == 1 else (p_o - p_e) / (1 - p_e)


def main(run: Path) -> None:
    labels = {l["id"]: l for l in json.loads((run / "labels.json").read_text())["labels"]}
    results = {r["id"]: r for r in json.loads((run / "correctness.json").read_text())["results"]}
    ids = sorted(labels)
    pairs = [(labels[i]["verdict"], results[i]["verdict"]) for i in ids]
    agree = sum(a == b for a, b in pairs)
    k = kappa(pairs)
    matrix = {exp: {got: sum(1 for a, b in pairs if a == exp and b == got) for got in VERDICTS} for exp in VERDICTS}
    disagreements = [
        {"id": i, "text": labels[i]["text"], "label": labels[i]["verdict"], "label_reason": labels[i]["reason"],
         "judge": results[i]["verdict"], "judge_rationale": results[i]["rationale"]}
        for i in ids if labels[i]["verdict"] != results[i]["verdict"]
    ]
    out = {"n": len(ids), "agreement": agree, "agreement_rate": round(agree / len(ids), 3), "cohen_kappa": round(k, 3),
           "confusion_matrix_rows_label_cols_judge": matrix, "disagreements": disagreements}
    (run / "agreement.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print(f"{agree}/{len(ids)} agree ({agree / len(ids):.0%}), Cohen's kappa = {k:.3f}")
    print(f"\n{'label \\ judge':<14}" + "".join(f"{v[:9]:>11}" for v in VERDICTS))
    for exp in VERDICTS:
        print(f"{exp:<14}" + "".join(f"{matrix[exp][got]:>11}" for got in VERDICTS))
    for d in disagreements:
        print(f"\n{d['id']} label {d['label']}, judge {d['judge']}: {d['text']}\n  label: {d['label_reason']}\n  judge: {d['judge_rationale']}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "runs/labeled_20"))
