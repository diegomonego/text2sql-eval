---
name: judge-correctness
description: Judge whether each question in a saved question file is relevant, answerable from the database, or ambiguous, with checked evidence and an overall correctness score. Use only when explicitly asked to run the correctness judge.
argument-hint: --questions <questions.json> --out <run-dir> [--db <url>] [--docs <dir> | --no-docs] [--anchor auto|off|YYYY-MM-DD]
disable-model-invocation: true
model: claude-opus-5-5
allowed-tools: Read, Write, Bash(uv run t2s *)
---

# Correctness judge

Arguments: $ARGUMENTS

You judge each question **on its text alone**, against the database and the docs. You don't see
how the questions were made or any labels they carry. You write links, verdicts and rationales; code
checks the links and computes the score. **Never write SQL.** Run only the `uv run t2s ...` commands
below; read with the Read tool, write with the Write tool. Work without asking questions.

Run each command exactly as written: no pipes, `;`, `&&` or `echo` (they are blocked). The command's own output says whether it succeeded and what to fix.

## Step 1: prepare

Run `uv run t2s judge-prepare --judge correctness $ARGUMENTS`. If it fails, report the error and stop.

## Step 2: read

Read in full `<run-dir>/work/correctness/brief.md`, then `<run-dir>/work/correctness/questions_for_judge.json`
(ids and texts only), the schema card and every docs file the brief lists. **Never open the question
file named in the arguments:** it may carry the generator's labels, and you must judge from the text alone.

## Step 3: judge every question

For each question, first link it (rules below), then pick the verdict. **Test the verdicts in this
order; the first that applies wins:**

| order | verdict | when |
|---|---|---|
| 1 | `OFF_TOPIC` | Not about the business the database describes. |
| 2 | `MISSING_DATA` | About the business, but at least one concept has no data and can't be derived from existing columns. |
| 3 | `AMBIGUOUS` | Two or more reasonable readings would give materially different answers, and the docs don't settle it. |
| 4 | `ANSWERABLE` | Every concept links to data, the linked tables connect, and there is one reasonable reading. |

- **Derived concepts** (e.g. profit, days late): `ANSWERABLE` if the docs define them or only one sensible derivation exists (state it in the rationale); `AMBIGUOUS` if several derivations are plausible; `MISSING_DATA` only when an ingredient doesn't exist.
- **Material difference** means the readings would change the answer: different columns, definitions or populations (e.g. "delay" as receipt minus commit date vs receipt minus ship date). Wording that every reasonable reader resolves the same way is not ambiguous.
- **Time:** if the brief says the time anchor is OFF, a question that depends on a relative period ("last quarter", "recently") is `AMBIGUOUS`. If it's ON, resolve the phrase with the brief's value.
- **No docs:** if the brief says no docs are supplied, a question that relies on what a coded column's values mean is `AMBIGUOUS`.
- **Rationale:** one or two sentences, grounded in the schema or docs (name the columns or doc section).

### Ambiguity checklist

Readers tend to settle on one reading too quickly. **Before choosing `ANSWERABLE`, go through this list.**
A question is `AMBIGUOUS` only if a second reading is reasonable, the docs don't settle it, and it would
change the answer.

1. **Which column or table:** for every column link, ask whether another column fits the phrase just as well. Examples: "date" on a line item could be the ship, commit or receipt date; "price" could be the retail price, the line's value or the order total; "country" could be the customer's or the supplier's. If one does, put it in `alternatives`.
2. **Stored or computed:** is there a stored value that answers it, and also a way to compute it from detail rows, with different results?
3. **Join or not:** does answering it with or without a join change who is counted? For example, all customers vs customers who placed orders.
4. **Scope:** which population or period is meant? For example, all orders or only shipped ones, per year or overall.
5. **Attachment:** what does each modifier attach to? In "suppliers in EUROPE with the highest revenue", is it revenue from European customers, or revenue of European suppliers?
6. **Vague filters:** "large", "recent", "top", "late" and similar, with no definition in the docs.
7. **Relative time:** see the time rule above.

If you rejected a close second reading, say so briefly in the rationale.

### Evidence each verdict needs (code checks this)

- `ANSWERABLE`: links for every concept; all links valid; no `missing` links; no `alternatives`.
- `AMBIGUOUS`: at least two `readings`, each with its own valid links (or one link with `alternatives`).
- `MISSING_DATA`: a `missing` link: `{"phrase": "satisfaction rating", "kind": "missing", "concept": "customer satisfaction rating", "closest": ["customer.c_acctbal"], "why_not": "no rating or feedback data exists"}`.
- `OFF_TOPIC`: a rationale.

### Link rules

Quote phrases exactly as they appear in the question (case may differ; `…` joins non-adjacent parts).
Link every concept: entities, measures, attributes, filter values, and the words that trigger each shape.

| kind | example |
|---|---|
| `table` | `{"phrase": "suppliers", "kind": "table", "table": "supplier"}` |
| `column` | `{"phrase": "shipped by AIR", "kind": "column", "columns": ["lineitem.l_shipmode"], "value": "AIR"}` |
| `column` (derived) | `{"phrase": "revenue", "kind": "column", "columns": ["lineitem.l_extendedprice", "lineitem.l_discount"], "source": "glossary: revenue"}` |
| `column` (ambiguous) | `{"phrase": "delay", "kind": "column", "columns": ["lineitem.l_receiptdate", "lineitem.l_commitdate"], "alternatives": [["lineitem.l_receiptdate", "lineitem.l_shipdate"]]}` |
| `shape` | `{"phrase": "never", "kind": "shape", "shape": "anti_join"}` |
| `missing` | see above |

For every column link, apply checklist item 1: another column that fits as well goes in `alternatives`.
Columns are `table.column`. Values: exact stored text (add `"match": "contains"` for a word inside
longer values); dates as `1997`, `1997-03`, `1997-03-15`, `1997-Q2` or `1993..1997`; numbers in stored
units. Never link `multi_join` (code derives it). Don't link join keys the question doesn't mention.

### Output

Write `<run-dir>/work/correctness/raw.json` with one result per question, in the file's order:

```json
{"results": [
  {"id": "q01", "verdict": "ANSWERABLE", "rationale": "…", "links": [ … ], "readings": []},
  {"id": "q02", "verdict": "AMBIGUOUS", "rationale": "…", "links": [ … ],
   "readings": [{"description": "delay = receipt minus commit date", "links": [ … ]},
                {"description": "delay = receipt minus ship date", "links": [ … ]}]}
]}
```

## Step 4: finalize

Run the finalize command printed at the end of the brief.

- **Exit 0:** done.
- **"FORMAT PROBLEMS"** or **"EVIDENCE PROBLEMS":** fix `raw.json` (correct the links, or change the verdict if the evidence shows it's wrong) and run it again. After 2 fixing rounds, if problems remain, run it once more with `--accept-issues` added; they will be flagged in the report.

## Step 5: reply

Reply with the finalize command's output only.
