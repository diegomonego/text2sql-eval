---
name: generate-questions
description: Generate exactly N realistic natural-language questions for evaluating a Text-to-SQL system on the configured database, with checked links to the schema. Use only when explicitly asked to generate an evaluation question set.
argument-hint: --n <N> --out <run-dir> [--db <url>] [--docs <dir> | --no-docs] [--preset coverage|natural] [--anchor auto|off|YYYY-MM-DD]
disable-model-invocation: true
model: claude-opus-5-5
allowed-tools: Read, Write, Bash(uv run t2s *)
---

# Generate evaluation questions

Arguments: $ARGUMENTS

You write candidate questions and link their phrases to the database. Code checks every link,
removes duplicates and selects exactly N. **Never write SQL.** Run only the `uv run t2s ...`
commands below; read files with the Read tool and write them with the Write tool. Work without
asking questions: nobody will answer.

Run each command exactly as written: no pipes, `;`, `&&` or `echo` (they are blocked). The command's own output says whether it succeeded and what to fix.

## Step 1: prepare

Run `uv run t2s gen-prepare $ARGUMENTS`. It prints the run directory. If it fails, report the error and stop.

## Step 2: read

Read in full: `<run-dir>/generation/brief.md` (preset, time anchor, shape legend, targets), then
`<run-dir>/generation/schema_card.md` (tables, columns, value ranges, listed values, joins), then every
docs file the brief lists (if it says no docs are supplied, rely on the schema card alone).

## Step 3: write one candidate per target

Write `<run-dir>/generation/candidates.json`:

```json
{"candidates": [
  {"target": "t01", "question": "…", "links": [ … ]}
]}
```

### Question rules

1. **Persona:** an analyst or manager at the business the docs describe (infer it from the schema if there are no docs), asking for something they need to know.
2. **Targeted candidates** must exercise the target's shape and, when the target names one, involve its focus table. **Free candidates** (`f…`): any question such a person would naturally ask.
3. **One analytical goal per question**, with the metric and scope stated ("by total order value", "in 1996", "for the BUILDING segment"). No compound questions joined by "and also".
4. **Business language only:** never table or column names (`l_shipmode`), never SQL words (join, group by, select, row, table, column).
5. **Real values:** filter values must exist in the data. Use the exact listed values from the schema card, phrased naturally ("the BUILDING segment", "shipped by AIR"). Dates must fall inside the data's range.
6. **Time:** use absolute periods ("in 1997", "between 1993 and 1996"). Only if the brief says the time anchor is ON may you use relative phrases ("last quarter"); then link them with the brief's resolved value.
7. **Follow the brief's preset section:** it says how far to spread across the schema and how simple to keep each question. Don't build questions on columns noted "constant in this data". If no docs are supplied, never use columns noted as coded.
8. **Natural combinations only:** combine shapes (e.g. a ranking of totals per region) only where a real analyst would ask it that way.
9. **Answerable:** never ask for data the database doesn't have. No trivia (one record's comment, internal IDs).
10. Use the docs' definitions (e.g. revenue) and name the metric the way the docs do.

### Link rules

Link every concept in the question: each entity, measure, attribute and filter value, plus the phrase
that triggers each shape. Quote phrases exactly as they appear in the question (case may differ); use
`…` to join parts that aren't adjacent.

| kind | when | example |
|---|---|---|
| `table` | the entity itself (listing or counting it) | `{"phrase": "suppliers", "kind": "table", "table": "supplier"}` |
| `column` | a measure, attribute or filter | `{"phrase": "shipped by AIR", "kind": "column", "columns": ["lineitem.l_shipmode"], "value": "AIR"}` |
| `column` (derived measure) | a measure computed from several columns | `{"phrase": "revenue", "kind": "column", "columns": ["lineitem.l_extendedprice", "lineitem.l_discount"], "source": "glossary: revenue"}` |
| `shape` | the words that make the question a given shape | `{"phrase": "never", "kind": "shape", "shape": "anti_join"}` |

- Columns are always `table.column`.
- **Values:** text = the exact stored value; add `"match": "contains"` for a word inside longer values (e.g. `"BRASS"` within part types). Dates = `1997`, `1997-03`, `1997-03-15`, `1997-Q2` or ranges like `1993..1997`. Numbers in stored units (a 5% discount is `0.05`).
- Link a shape for every shape the question exercises, using the legend's ids. **Never link `multi_join`**: code derives it from the tables.
- Don't link join keys or tables the question doesn't mention; code finds the join path.
- Never use `missing` links or `alternatives` here: if a concept can't be linked cleanly, change the question.

## Step 4: check and select

Run `uv run t2s gen-select --out <run-dir>`.

- **Exit 0:** done. The question file is written.
- **"NOT ENOUGH CANDIDATES":** write new candidates for the listed targets to the file it names
  (e.g. `candidates_round2.json`), same format, fixing the drop reasons it prints. Then run gen-select again.
  At most 2 extra rounds.
- **Format error:** fix the JSON file and run gen-select again.

## Step 5: reply

Reply with gen-select's final summary only.
