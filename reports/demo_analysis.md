# Demonstration cases: analysis

All cases use the same database instance (TPC-H SF 0.1 in DuckDB, `data/tpch_sf01.duckdb`) and the same documents (`semantic_docs/tpch`: glossary plus TPC-H spec extracts). Run folders are under `runs/`; `uv run t2s check-run <folder>` confirms that a folder's files agree (same database, docs and config; judges ran on the current question file).

## Case 1: small budget (N = 5)

Run: `runs/v2_n5` (coverage preset, the default). Command: `make generate N=5 RUN=runs/v2_n5`, then the judges.

**What the generator did.** It wrote 21 candidates, one per target (16 targeted slots plus 5 free-form). All passed the code checks, with no duplicates and no extra rounds. Greedy selection then picked 5:

| Pick | Question | Shapes | Gain |
|---|---|---|---|
| q01 | How many line items from suppliers in the UNITED KINGDOM were received late in each year from 1993 to 1997? | aggregation, multi_join, time_trend | 0.308 |
| q02 | How many customers in the MIDDLE EAST region have never placed an order? | aggregation, anti_join, multi_join | 0.224 |
| q03 | What percentage of revenue from orders placed by customers in INDONESIA last year came from items shipped by TRUCK? | multi_join, ratio | 0.105 |
| q04 | Which 3 container types accounted for the largest quantity of units shipped this year? (free-form slot) | ranking | 0.098 |
| q05 | List the names and phone numbers of suppliers in the ASIA region whose account balance is above that region's supplier average. | multi_join, vs_aggregate | 0.082 |

The rows are in pick order, and q01–q05 are the IDs in `questions.json`. Together the five cover 7 of 8 tables, 14 of 61 columns and 7 of 8 shapes. The whole pool reached 30 columns.

**The trade-off: shapes over tables.** With five slots the generator can't cover everything, and the gain formula counts shapes for half of a question's value (λ = 0.5 / 0.25 / 0.25). So it spent the budget on seven different shapes and gave up two things:

- **The `partsupp` table** (supply cost, available quantity). The best candidate for it, c003, "What is the total available quantity of Brand#35 parts across suppliers based in GERMANY?", came a close second twice:
  - in round 3, 0.103 against 0.105 for the ratio question;
  - in round 4, 0.095 against 0.098 for the ranking question.

  Each time, a new shape (ratio, then ranking) was worth slightly more than a new table and its columns.
- **The `lookup` shape.** It has the lowest weight in the legend (W = 0.60, since nearly every system handles simple lookups). The two lookup candidates never came close: the best ranked 4th in the last round, with 0.062 against 0.082.

**This is the objective's choice, not a greedy shortcut.** Checking every possible 5-question subset of the pool (all 20,349 of them) finds the same set as greedy (`generation/diagnostics.json`). Weighting the three dimensions equally makes the opposite trade-off: it swaps the anti-join and ranking questions for two that bring in `partsupp`, ending with 8 tables and 16 columns but only 6 shapes. The setting is deliberate. Query shapes are where Text-to-SQL systems differ most, and every table gets used again as N grows.

*Judge results for this case are added below once the judges have run.*

## Case 2: larger budget (N = 15)

Run: `runs/v2_n15`. *Analysis to follow the judge runs.*

## Case 3: controlled check

Runs:
- `runs/v2_n15`: the baseline, the original 15 questions;
- `runs/v2_n15_repeat`: the same file judged again, to measure repeatability;
- `runs/v2_n15_controlled`: the edited copy.

### The edits

The edited copy is `runs/v2_n15_controlled/questions.json`. It is the 15 questions of `v2_n15` with two replaced, keeping their IDs. The replacements are hand-written and carry no generator labels, as a reviewer's edit would.

| ID | Original question | Replacement | Why |
|---|---|---|---|
| q04 | For customers in the MIDDLE EAST region, what percentage of line items shipped in 1997 went by AIR? | **How many orders were cancelled in 1997?** | On topic, but the database has no cancellations. Order status only takes the values fulfilled, open or partially fulfilled (F/O/P, defined in the glossary). This is a near miss: a status column exists, but not this status. |
| q15 | What share of revenue from orders placed in 1997 came from customers in CHINA? | **Between 1993 and 1997, how many orders did customers in the AUTOMOBILE segment place each year?** | A paraphrase of q13, which stays in the set: "How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997?" |

**Why these two slots.** In the baseline coverage report, q04 and q15 are among the four questions that cover nothing unique. Removing both loses no table, column or shape. So any change in the reports comes from what the new questions are, not from what the old ones covered.

### Repeatability (measured before the edit)

The unchanged file was judged twice (`v2_n15` and `v2_n15_repeat`):

- **Correctness:** the same verdict for all 15 questions (all `ANSWERABLE`), score 1.00 both times. The judge's links were worded differently in 7 of 15 questions, with different phrase boundaries, without changing any verdict.
- **Coverage:** the same credited tables, columns and shapes for every question. Score 80.87 both times: 8/8 tables, 26/61 columns, 8/8 shapes. The same four questions covered nothing unique (q01, q03, q04, q15).

So on this set, differences larger than wording variation can be attributed to the edits.

### Expectations (written and committed before the judges ran on the edited copy)

**Correctness judge**

| | Baseline | Expected |
|---|---|---|
| q04 (cancelled orders) | `ANSWERABLE` (original question) | **`MISSING_DATA`**. The missing concept is order cancellation, and the closest column is `orders.o_orderstatus`, whose values (F/O/P) have no cancelled state |
| q15 (paraphrase of q13) | `ANSWERABLE` (original question) | **`ANSWERABLE`**, the same as q13 |
| The other 13 | `ANSWERABLE` | `ANSWERABLE` (unchanged, as the repeat run suggests) |
| Score | (15 + 0.5 × 0) / 15 = 1.00 | **(14 + 0.5 × 0) / 15 = 0.93** |

**Coverage judge**

| | Baseline | Expected |
|---|---|---|
| Tables / columns / shapes | 8/8, 26/61, 8/8 | **unchanged: 8/8, 26/61, 8/8** |
| Score | 80.87 | **80.87 (unchanged)** |
| Questions earning no credit | none | **q04**, because it has a concept with no data |
| Duplicate pairs | none | **q13 = q15**: the same tables (customer, orders), columns (`c_mktsegment`, `o_orderdate`) and shapes (aggregation, time_trend) |
| Questions covering nothing unique | q01, q03, q04, q15 | **q03, q13, q15**. q13 and q15 now share everything. q04 earns no credit at all. q01 leaves the list because, with the original q15 gone, it is the only question covering `nation.n_name` |

**Labels:** q04 and q15 carry no labels, so the judges report no label check for them. `check-run` notes that the file is no longer fully labeled.

**What would count as a miss, and why it might happen:**

- **The correctness judge calls q04 `AMBIGUOUS` or `ANSWERABLE`,** for example by guessing that some status value means cancelled. The glossary rules that out, so this would be a judge error.
- **The coverage judge links the paraphrase differently from q13,** for example missing "each year" as the time-trend trigger or adding an extra column. The pair would then not be flagged, and q13 would keep something unique. Coverage would still be unchanged. This is the known weak point of detecting duplicates by link signature.
- **The coverage judge credits q04 anyway,** with no `missing` link. q04's credit would then show up in the report.

The score is expected to drop for correctness (one of 15 questions can't be answered) and to stay the same for coverage. A paraphrase adds no coverage, and an unanswerable question earns none, so the set covers exactly what it did before.

### Results

*Added after the run, below this line; the expectations above are left as committed.*
