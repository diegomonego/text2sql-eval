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

**What the judges report** (`runs/v2_n5/correctness.md`, `coverage.md`):

- **Correctness: 1.00.** All 5 are `ANSWERABLE`, (5 + 0.5 × 0) / 5. Every rationale is grounded in the schema and glossary, and the judge names the close second reading it rejected, as its ambiguity checklist asks. Two examples:
  - q03: revenue is the glossary's `l_extendedprice × (1 − l_discount)`. "o_totalprice was rejected since it includes tax and cannot be split by ship mode".
  - q04: "Reading 'container type' as only the kind word (BOX, BAG…) was rejected: the glossary defines the container as the single p_container value".
- **Coverage: 65.98** = (87.5 + 22.95 + 87.5) / 3. Tables 7/8 (missing `partsupp`), columns 14/61, shapes 7/8 (missing `lookup`).
  - No duplicate pairs, and every question covers something no other question does. At N = 5 there is no repetition.
  - The budget note puts the ceiling at about 16 columns for 5 questions (3.2 columns per question). The set reached 14.
  - The judge's verified coverage equals the generator's claimed coverage on every dimension (`check-run`).
- **The same score as v1, reached differently.** The v1 N = 5 set also scored 65.98, but with 8/8 tables and only 6/8 shapes. Averaging hides that difference, which is why the report leads with the three dimensions and puts the summary score last.

## Case 2: larger budget (N = 15)

Run: `runs/v2_n15` (coverage preset). Command: `make generate N=15 RUN=runs/v2_n15`, then the judges.

The generator wrote 45 candidates (30 targeted, 15 free-form). All passed the checks, with no duplicates. Greedy reached 100% of the best subset found by a swap search.

| | N = 5 | N = 15 |
|---|---|---|
| Correctness | 1.00 (5 answerable) | 1.00 (15 answerable) |
| Tables | 7/8 | **8/8** |
| Columns | 14/61 (22.95%) | **26/61 (42.62%)** |
| Shapes | 7/8 | **8/8** |
| Coverage score | 65.98 | 80.87 |
| Column ceiling at this N (budget note) | ~16 | ~41 |
| Duplicate pairs | none | none |
| Questions covering nothing unique | none | 4 (q01, q03, q04, q15) |

**What gained coverage.**

- **The `partsupp` table** and the **`lookup` shape**, the two things the five-question set gave up. q02 and q12 bring in `partsupp`. q02, q08 and q14 are simple lookups.
- **14 more columns,** most of them the less obvious attributes the coverage preset pushes toward: account balance, market segment, return flag, shipping instruction, tax, clerk, order priority and status, order value, brand, part name, retail price, available quantity, supply cost.

**Two columns covered at N = 5 are missing at N = 15:** `l_commitdate` and `s_phone`. Each run generates a fresh pool from the database, docs and N, so the N = 15 set is not a superset of the N = 5 set. That is deliberate (no hidden shared pool between cases), and it means comparisons are between two independent samples.

**Where repetition appears.** There are no duplicate pairs, but reuse concentrates on a few items, which is expected once every shape and table is covered:

- `customer` and `lineitem` each appear in 8 of 15 questions, `orders` in 6;
- `aggregation` in 8 and `multi_join` in 7.

Four questions add nothing unique: q01, q03, q04 and q15. Every table, column and shape they touch is also covered elsewhere. They still earn their place under the selection objective, because they repeat high-weight shapes (a time trend, an anti-join, two ratios), but a reviewer looking for slack would start there. Case 3 replaces two of them.

**What remains uncovered: 35 of 61 columns.**

- **23 are join keys (15) and comments (8).** The generator's realism rules avoid them on purpose: keys aren't business concepts, and TPC-H comments are generated filler text. Coverage is still defined over the whole schema, so they stay visible as gaps.
- **The other 12 are real gaps, for different reasons:**
  - **names and phones:** `c_name`, `c_phone`, `s_phone`;
  - **dates and part attributes:** `l_commitdate` (covered at N = 5), `p_mfgr`, `p_type`, `p_size`;
  - **coded:** `l_linestatus`;
  - **constant in this data:** `o_shippriority`;
  - **free text and line numbers:** `c_address`, `s_address`, `l_linenumber`.

  The budget note says about 41 columns could be covered at 2.7 columns per question. Reaching more would take questions about those attributes, or a larger N.

## Tracing one question from generation through both judges

This traces question **q13** of `runs/v2_n15`: *"How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997?"*

| Step | File | What it shows |
|---|---|---|
| 1. Slot | `generation/targets.json` | Target `t05`: a targeted slot asking for a `time_trend` question with focus table `customer` |
| 2. Candidate | `generation/pool.json` (candidate `c005`) | The LLM's question and 5 links: "number of" → aggregation; "orders" → table `orders`; "customers in the AUTOMOBILE segment" → `customer.c_mktsegment` = AUTOMOBILE; "year by year" → time_trend; "between 1993 and 1997" → `orders.o_orderdate` = 1993..1997 |
| 3. Code checks | `generation/pool.json` | All 5 links pass: the phrases are in the question, the columns exist, AUTOMOBILE exists, and 1993..1997 is within the data's range. Derived: tables customer and orders, joined directly, so no multi_join |
| 4. Selection | `generation/pick_log.json` | Ranked 15th in round 1 (gain 0.204 against 0.339 for the pick). Picked in **round 13** with gain 0.0226: 0.0185 for repeating aggregation and time_trend, and 0.0041 for `c_mktsegment`, its only new item. That beat candidate c001's 0.0206. IDs follow pick order, hence q13 |
| 5. Question file | `questions.json` | The labels: tables customer and orders; columns `c_mktsegment` and `o_orderdate`; shapes aggregation and time_trend |
| 6. Judge input | `work/*/questions_for_judge.json` | Only the ID and text. The labels are stripped |
| 7. Correctness judge | `correctness.json` / `.md` | Its own 6 links, all passing. **ANSWERABLE**: "Counts orders per year of orders.o_orderdate (1993..1997) for customers with customer.c_mktsegment = 'AUTOMOBILE'. The order date is the only sensible date for counting orders by year." All 6 labels confirmed. It contributes 1 to (15 + 0.5 × 0) / 15 = 1.00 |
| 8. Coverage judge | `coverage.json` / `.md` | Its own 6 links, all passing, each with one target. Credited: tables customer and orders; columns `c_mktsegment` and `o_orderdate`; shapes aggregation and time_trend. **Unique: `customer.c_mktsegment`**, which no other question covers. All labels confirmed |
| 9. Into the scores | `coverage.md` | q13 is the only question covering `c_mktsegment`, one of the 26 covered columns, and is listed under aggregation and time_trend in the item map. The score: (100 + 42.62 + 100) / 3 = 80.87 |
| 10. Case 3 | `runs/v2_n15_controlled` | A paraphrase of q13 replaced q15. As predicted, the coverage judge flagged q13 = q15 as a duplicate pair, and q13 lost its unique item |

The same path works for any question: find its candidate by `question_id` in `pool.json`, its round in `pick_log.json`, and the same `id` in both judge reports. `uv run t2s check-run <run>` confirms the files belong together.

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

Both judges ran on `runs/v2_n15_controlled` at 11:51–11:54, after the expectations were committed at 11:51 (commit `7cd8279`). `check-run` passes, and notes that the file no longer carries generator labels for every question.

**Every expectation was met.**

| Expectation | Result |
|---|---|
| q04 → `MISSING_DATA`, closest `orders.o_orderstatus` | ✅ `MISSING_DATA`. Missing concept "order cancellation", closest columns `o_orderstatus` **and** `l_returnflag`. The rationale: "o_orderstatus is F/O/P (fulfilled, open, partially fulfilled per the glossary) and lineitem.l_returnflag records returns, not cancellations." The judge also ruled out a second near miss we hadn't listed. |
| q15 → `ANSWERABLE` | ✅ `ANSWERABLE`, with the same reading as q13 (orders per year of `o_orderdate` for AUTOMOBILE customers) |
| The other 13 unchanged | ✅ all `ANSWERABLE` |
| Correctness 1.00 → 0.93 | ✅ (14 + 0.5 × 0) / 15 = 0.9333 |
| Coverage unchanged at 80.87 | ✅ 8/8 tables, 26/61 columns, 8/8 shapes: (100 + 42.62 + 100) / 3 = 80.87 |
| q04 earns no credit | ✅ Listed under "questions earning no credit". Its orders table, order date and aggregation shape are shown as not credited because "concept not in the database: order cancellation". The budget note now says 1 question earned no credit. |
| Duplicate pair q13 = q15 | ✅ Flagged. The coverage judge linked both to tables customer and orders, columns `c_mktsegment` and `o_orderdate`, and shapes aggregation and time_trend, even though their wording differs ("change year by year" vs "each year", "number of orders" vs "how many") |
| Nothing unique: q03, q13, q15 | ✅ Exactly. q13 lost its unique column `c_mktsegment` to the paraphrase, and q01 left the list because it is now the only question covering `nation.n_name` |

**What this shows.**

- **The correctness judge** separates an on-topic question with missing data from answerable ones, and backs the verdict with checkable evidence: the missing concept, the closest columns, and why they don't fit. The score drops by exactly that question's share.
- **The coverage judge** confirms what the exercise anticipated: a paraphrase stays fully answerable while adding no coverage. The score staying at 80.87 is correct, not a blind spot. The report shows the change where it belongs: a new duplicate pair, a question earning nothing, and a shorter list of questions with unique coverage.
- **The duplicate rule caught this paraphrase** because both questions were linked to the same items. A paraphrase whose synonyms led to different links would not have been caught; that remains the known weak point.
- **Cost:** $0.73 for the correctness judge and $0.57 for the coverage judge.

## Judge validation: 20 labeled questions

Run: `runs/labeled_20`. The question file has the questions only; the expected verdicts are in `labels.json`. Agreement is computed by `python3 validation/judge_agreement.py runs/labeled_20`, which writes `agreement.json`.

**The set.** 20 questions written to cover all four verdicts:
- 8 on-topic but unanswerable;
- 5 ambiguous;
- 5 answerable: three paraphrases with synonyms, and two questions from the TPC-H SF 0.01 robustness run;
- 2 off-topic.

Two were deliberately borderline: "Which shipping mode should we recommend for fragile parts?" (labeled `MISSING_DATA`: on topic, but fragility isn't recorded) and "What is the population of GERMANY?" (labeled `OFF_TOPIC`: it names a nation in the data, but isn't a business question). The questions were shuffled so that verdict types aren't grouped.

**How the labels were made.** The labels were drafted by Claude, the same model family as the judge, from the rationales written when the questions were designed, and approved by the user. They are not independent human labels: agreement means the judge matches the approved reasoning.

To rule out adjusting the labels after the fact:
- they were fixed before the judge ran, with SHA-256 `8fad20afcea03dd5dbda61ae1322f9cefc5a3720ecc2f06503acde5b12a6479a`, which matches the committed `labels.json`;
- they were kept outside the repository during the run, since judges can read files beyond their inputs.

**Results: 19 of 20 agree (95%), Cohen's κ = 0.93.**

| Label \ Judge | OFF_TOPIC | MISSING_DATA | AMBIGUOUS | ANSWERABLE |
|---|---|---|---|---|
| OFF_TOPIC | 1 | **1** | 0 | 0 |
| MISSING_DATA | 0 | 8 | 0 | 0 |
| AMBIGUOUS | 0 | 0 | 5 | 0 |
| ANSWERABLE | 0 | 0 | 0 | 5 |

**The one disagreement is the borderline case flagged in advance.** For "What is the population of GERMANY?", the judge said `MISSING_DATA`: "GERMANY is a nation.n_name value, but the nation table holds only key, name, region and filler comment; no population or demographic data exists." It treated a question that names an entity in the data as on topic. Both verdicts score 0, so the correctness score is the same either way. What it shows is that the line between `OFF_TOPIC` and `MISSING_DATA` is fuzzy for questions near the domain. The verdict definitions could say explicitly that naming a database entity doesn't make a question on topic.

**What went right, beyond the counts.**

- **All five ambiguous questions were caught,** the known weak spot of LLM judges. Each came with checked readings:
  - **"How many line items did we have in March 1996?":** three readings (order, ship and receipt date).
  - **"What is the average price of a part?":** three readings, one more than the label listed (list price, supply cost, and realized selling price). The judge added that the averages differ "a lot (about 1,400 vs about 500)".
- **The hardest near miss was recognized as missing data:** "How did the available quantity of Brand#23 parts change month by month during 1997?" The judge noted that `ps_availqty` "is one undated value per part and supplier. No inventory history exists".
- **The borderline "fragile parts" question was `MISSING_DATA`, as labeled:** "nothing marks parts as fragile (p_type and p_container describe finish, material and packaging), and no damage or breakage outcomes exist to base a recommendation on."
- **The paraphrases with synonyms were answered correctly,** with the alternatives considered and rejected. For "paid the most in total once tax is included", the judge used the order total "which the glossary … and spec 4.2.3 define as the sum of line charges including tax", and "rejected filtering by ship date, since payment attaches to the order".

**Limits of this check.**
- **Twenty questions give a rough estimate.** One disagreement moves agreement by 5 points.
- **The set is deliberately weighted toward failures:** 15 of 20 are not answerable. So agreement here says how well the judge tells failure types apart, not how it behaves on typical generated sets, where almost every question is answerable.
- **The labels share the judge's model family.** An independent human labeling remains the stronger test.
- **Only the correctness judge was validated this way.** The coverage judge's links were checked through the controlled check and the claimed-vs-verified comparison, not against labels.
