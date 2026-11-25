# Generation brief

N = 15. Pool: 30 targeted + 15 free = 45 candidates (one per target below).
Code will check every candidate, remove duplicates and select exactly 15.

## Files to read
- `runs/n15/generation/schema_card.md`: tables, columns, value ranges, listed values, joins.
- Docs: Read every one of these documents in full:

- `semantic_docs/tpch/glossary.md`
- `semantic_docs/tpch/spec/clause1_database_design.md`
- `semantic_docs/tpch/spec/clause4_data_generation.md`

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
| `t01` | targeted | lookup | lineitem |
| `t02` | targeted | aggregation | orders |
| `t03` | targeted | multi_join | partsupp |
| `t04` | targeted | ranking | part |
| `t05` | targeted | time_trend | customer |
| `t06` | targeted | ratio | supplier |
| `t07` | targeted | vs_aggregate | nation |
| `t08` | targeted | anti_join | region |
| `t09` | targeted | lookup | orders |
| `t10` | targeted | aggregation | partsupp |
| `t11` | targeted | multi_join | part |
| `t12` | targeted | ranking | customer |
| `t13` | targeted | time_trend | supplier |
| `t14` | targeted | ratio | nation |
| `t15` | targeted | vs_aggregate | region |
| `t16` | targeted | anti_join | lineitem |
| `t17` | targeted | lookup | partsupp |
| `t18` | targeted | aggregation | part |
| `t19` | targeted | multi_join | customer |
| `t20` | targeted | ranking | supplier |
| `t21` | targeted | time_trend | nation |
| `t22` | targeted | ratio | region |
| `t23` | targeted | vs_aggregate | lineitem |
| `t24` | targeted | anti_join | orders |
| `t25` | targeted | lookup | part |
| `t26` | targeted | aggregation | customer |
| `t27` | targeted | multi_join | supplier |
| `t28` | targeted | ranking | nation |
| `t29` | targeted | time_trend | region |
| `t30` | targeted | ratio | lineitem |
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
| `f11` | free | - | - |
| `f12` | free | - | - |
| `f13` | free | - | - |
| `f14` | free | - | - |
| `f15` | free | - | - |

## Output
Write all candidates to `runs/n15/generation/candidates.json`, then run:
`uv run t2s gen-select --out runs/n15`
