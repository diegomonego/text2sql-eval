---
name: judge-coverage
description: Measure how well a saved question file covers the database's tables, columns and query shapes, with checked links, repetition and an overall coverage score. Use only when explicitly asked to run the coverage judge.
argument-hint: --questions <questions.json> --out <run-dir> [--no-docs] [--anchor auto|off|YYYY-MM-DD]
disable-model-invocation: true
model: claude-opus-5-5
allowed-tools: Read, Write, Bash(uv run t2s *)
---

# Coverage judge

Arguments: $ARGUMENTS

You link each question's phrases to the database, **from the question text alone**. You don't see
how the questions were made or any labels they carry. Code checks your links, decides what earns
coverage credit, finds repetition and computes the score. **Never write SQL.** Run only the
`uv run t2s ...` commands below; read with the Read tool, write with the Write tool. Work without
asking questions.

Run each command exactly as written: no pipes, `;`, `&&` or `echo` (they are blocked). The command's own output says whether it succeeded and what to fix.

## Step 1: prepare

Run `uv run t2s judge-prepare --judge coverage $ARGUMENTS`. If it fails, report the error and stop.

## Step 2: read

Read in full `<run-dir>/work/coverage/brief.md`, then `<run-dir>/work/coverage/questions_for_judge.json`
(ids and texts only), the schema card and every docs file the brief lists. **Never open the question
file named in the arguments:** it may carry the generator's labels, and you must link from the text alone.

## Step 3: link every question

Link what each question **actually asks for**: every entity, measure, attribute and filter value it
mentions, plus the words that trigger each shape it exercises. Be faithful, not generous:

- Don't add tables or columns a query might need but the question doesn't mention (join keys earn nothing; code finds the join path).
- If a phrase could reasonably mean two or more different columns or definitions that the docs don't settle, give the main reading in `columns` and the others in `alternatives`. Ambiguous phrases earn no credit.
- If a concept has no data in the database, add a `missing` link. A question with a missing concept earns no credit.
- If the question isn't about this business at all, give it no links and say so in `note`.
- Time: if the brief says the time anchor is OFF, a relative period ("last quarter") is ambiguous: use `alternatives`. If it's ON, use the brief's resolved value.
- No docs: if the brief says no docs are supplied, a phrase that relies on what a coded column's values mean is ambiguous.

### Link rules

Quote phrases exactly as they appear in the question (case may differ; `…` joins non-adjacent parts).

| kind | example |
|---|---|
| `table` | `{"phrase": "suppliers", "kind": "table", "table": "supplier"}` |
| `column` | `{"phrase": "shipped by AIR", "kind": "column", "columns": ["lineitem.l_shipmode"], "value": "AIR"}` |
| `column` (derived) | `{"phrase": "revenue", "kind": "column", "columns": ["lineitem.l_extendedprice", "lineitem.l_discount"], "source": "glossary: revenue"}` |
| `column` (ambiguous) | `{"phrase": "delay", "kind": "column", "columns": ["lineitem.l_receiptdate", "lineitem.l_commitdate"], "alternatives": [["lineitem.l_receiptdate", "lineitem.l_shipdate"]]}` |
| `shape` | `{"phrase": "never", "kind": "shape", "shape": "anti_join"}` |
| `missing` | `{"phrase": "satisfaction rating", "kind": "missing", "concept": "customer satisfaction rating", "closest": ["customer.c_acctbal"], "why_not": "no rating data exists"}` |

Columns are `table.column`. Values: exact stored text (add `"match": "contains"` for a word inside
longer values); dates as `1997`, `1997-03`, `1997-03-15`, `1997-Q2` or `1993..1997`; numbers in stored
units. Use the legend's shape ids, and link a shape only when the question's wording calls for it (a
date used only as a filter is not a time trend). Never link `multi_join` (code derives it).

### Output

Write `<run-dir>/work/coverage/raw.json` with one result per question, in the file's order:

```json
{"results": [
  {"id": "q01", "links": [ … ], "note": "optional, one short sentence"}
]}
```

## Step 4: finalize

Run the finalize command printed at the end of the brief.

- **Exit 0:** done.
- **"FORMAT PROBLEMS"** or **"EVIDENCE PROBLEMS":** fix `raw.json` and run it again. After 2 fixing rounds, if problems remain, run it once more with `--accept-issues` added; they will be flagged in the report.

## Step 5: reply

Reply with the finalize command's output only.
