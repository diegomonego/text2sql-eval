# Generation brief

N = 5. Pool: 16 targeted + 10 free = 26 candidates (one per target below).
Code will check every candidate, remove duplicates and select exactly 5.

## Files to read
- `runs/v2_n5_natural/generation/schema_card.md`: tables, columns, value ranges, listed values, joins.
- Docs: Read every one of these documents in full:

- `semantic_docs/tpch/glossary.md`
- `semantic_docs/tpch/spec/clause1_database_design.md`
- `semantic_docs/tpch/spec/clause4_data_generation.md`

## Preset
**natural**: everyday questions.

- **Write each question the way it would arrive in a ticket or a chat message** from a colleague: one ask, plainly worded.
- **Don't stack extra filters or conditions just to reach more columns.** A natural question that reuses common columns beats a contrived one.
- **At most 2 shapes per question.** Code drops candidates with more. The derived `multi_join` counts: a question that needs 3 or more tables already uses one of the 2.
- **Targets name a shape only.** Choose whatever tables make the question natural.
- **Free candidates carry extra weight:** at least 1 of the 5 picks must come from them. Make them the questions this business asks most often.

## Time anchor
**Time anchor: ON, 1998-08-02** (the latest `orders.o_orderdate`). Relative phrases resolve as follows; use the value column as the link value:

| phrase | from | to | link value |
|---|---|---|---|
| this year | 1998-01-01 | 1998-08-02 | `1998` |
| last year | 1997-01-01 | 1997-12-31 | `1997` |
| this quarter | 1998-07-01 | 1998-08-02 | `1998-Q3` |
| last quarter | 1998-04-01 | 1998-06-30 | `1998-Q2` |
| this month | 1998-08-01 | 1998-08-02 | `1998-08` |
| last month | 1998-07-01 | 1998-07-31 | `1998-07` |
| last 12 months | 1997-08-03 | 1998-08-02 | `1997-08-03..1998-08-02` |

## Shape legend (use these ids in shape links)
| id | name | what it means | trigger words (examples) | example question |
|---|---|---|---|---|
| `lookup` | Simple lookup | Retrieves facts about specific records from one table, with no aggregate. | what is, which, list, show | What is the account balance and phone number of Supplier#000000042? |
| `aggregation` | Aggregation | Computes a total, count, average, minimum or maximum, overall or per group. | total, how many, average, number of, per, by | What is the total order value per market segment? |
| `multi_join` | Join (3+ tables) **(derived by code: never link it)** | Needs data from three or more tables. Derived by code from the tables the question links and the join path between them. | - | What is the total revenue per region? |
| `ranking` | Ranking / top-K | Asks for the highest or lowest N items, overall or within each group. | top, highest, lowest, most, least, best, largest | Who are the 10 customers with the highest total order value? |
| `time_trend` | Time trend / period comparison | Groups by time periods (month, quarter, year) or compares periods. A date used only as a filter does not count. | per month, each quarter, by year, over time, trend, year over year, compared with | How did total order value change month by month in 1997? |
| `ratio` | Ratio / share of total | Computes a share, percentage, proportion or rate (part divided by a whole). | share, percentage, proportion, fraction, rate, ratio | What share of total order value comes from the BUILDING segment? |
| `vs_aggregate` | Comparison against an aggregate | Compares records with an aggregate of a group (above or below average, more than the median). | above average, below average, more than the average, higher than typical | Which suppliers have an account balance above the average for their nation? |
| `anti_join` | Anti-join | Asks for records that have no matching record elsewhere. | never, without, no orders, not ... any, none | Which customers have never placed an order? |

## Targets
| target | kind | shape | focus table |
|---|---|---|---|
| `t01` | targeted | lookup | - |
| `t02` | targeted | aggregation | - |
| `t03` | targeted | multi_join | - |
| `t04` | targeted | ranking | - |
| `t05` | targeted | time_trend | - |
| `t06` | targeted | ratio | - |
| `t07` | targeted | vs_aggregate | - |
| `t08` | targeted | anti_join | - |
| `t09` | targeted | lookup | - |
| `t10` | targeted | aggregation | - |
| `t11` | targeted | multi_join | - |
| `t12` | targeted | ranking | - |
| `t13` | targeted | time_trend | - |
| `t14` | targeted | ratio | - |
| `t15` | targeted | vs_aggregate | - |
| `t16` | targeted | anti_join | - |
| `f01` | free | - | - |
| `f02` | free | - | - |
| `f03` | free | - | - |
| `f04` | free | - | - |
| `f05` | free | - | - |
| `f06` | free | - | - |
| `f07` | free | - | - |
| `f08` | free | - | - |
| `f09` | free | - | - |
| `f10` | free | - | - |

## Output
Write all candidates to `runs/v2_n5_natural/generation/candidates.json`, then run:
`uv run t2s gen-select --out runs/v2_n5_natural`
