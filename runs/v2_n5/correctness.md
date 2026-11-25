# Correctness report

- Generated: 2026-11-25T15:05:31+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 7cd82794b736dc1a0b94a142382d6c4310cd0cbb
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/v2_n5/questions.json, questions_sha256=f59d3d75ef786c7cb1ff69bf624637f25f15cc7efb3fd2fd2dc32dff75d56aef, n=5, issues_accepted=0

## Score

**1.0000** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (5 + 0.5 x 0) / 5 = 1.0000

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 0 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 5 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | How many line items from suppliers in the UNITED KINGDOM were received late in each year from 1993 to 1997? | **ANSWERABLE** | Supplier nation via supplier.s_nationkey -> nation.n_name; 'received late' is the glossary's late delivery (l_receiptdate > l_commitdate), counted per year of l_receiptdate for 1993-1997. Grouping by order or ship year was rejected because the question ties the year to 'received'. |
| q02 | How many customers in the MIDDLE EAST region have never placed an order? | **ANSWERABLE** | Customer region via customer.c_nationkey -> nation.n_regionkey -> region.r_name = 'MIDDLE EAST'; 'never placed an order' means no row in orders with o_custkey = c_custkey (spec clause 1.4 notes a third of customers have no orders). |
| q03 | What percentage of revenue from orders placed by customers in INDONESIA last year came from items shipped by TRUCK? | **ANSWERABLE** | Revenue is the glossary's l_extendedprice * (1 - l_discount); population is lines of orders with o_orderdate in 1997 (last year, time anchor ON) from customers whose nation is INDONESIA, and the share is the part with l_shipmode = 'TRUCK'. o_totalprice was rejected since it includes tax and cannot be split by ship mode. |
| q04 | Which 3 container types accounted for the largest quantity of units shipped this year? | **ANSWERABLE** | Sum lineitem.l_quantity per part.p_container for lines with l_shipdate in 1998 (this year, time anchor ON) and return the top 3. Reading 'container type' as only the kind word (BOX, BAG...) was rejected: the glossary defines the container as the single p_container value. |
| q05 | List the names and phone numbers of suppliers in the ASIA region whose account balance is above that region's supplier average. | **ANSWERABLE** | Suppliers whose nation is in region.r_name = 'ASIA' (supplier.s_nationkey -> nation -> region), returning s_name and s_phone where s_acctbal exceeds the average s_acctbal of all ASIA suppliers. |

## Evidence

### q01: ANSWERABLE

> How many line items from suppliers in the UNITED KINGDOM were received late in each year from 1993 to 1997?

Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "UNITED KINGDOM" → nation.n_name = `UNITED KINGDOM`<br>✓ "received late" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "in each year" → shape `time_trend`<br>✓ "from 1993 to 1997" → lineitem.l_receiptdate = `1993..1997`

- Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:nation.n_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q02: ANSWERABLE

> How many customers in the MIDDLE EAST region have never placed an order?

Links: ✓ "How many" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "never" → shape `anti_join`<br>✓ "placed an order" → orders

- Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q03: ANSWERABLE

> What percentage of revenue from orders placed by customers in INDONESIA last year came from items shipped by TRUCK?

Links: ✓ "What percentage" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders" → orders<br>✓ "placed … last year" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "INDONESIA" → nation.n_name = `INDONESIA`<br>✓ "items" → lineitem<br>✓ "shipped by TRUCK" → lineitem.l_shipmode = `TRUCK`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipmode confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q04: ANSWERABLE

> Which 3 container types accounted for the largest quantity of units shipped this year?

Links: ✓ "Which 3 … largest" → shape `ranking`<br>✓ "container types" → part.p_container<br>✓ "accounted for" → shape `aggregation`<br>✓ "quantity of units" → lineitem.l_quantity<br>✓ "shipped this year" → lineitem.l_shipdate = `1998`

- Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_container confirmed, shapes:ranking confirmed, shapes:aggregation not labeled

### q05: ANSWERABLE

> List the names and phone numbers of suppliers in the ASIA region whose account balance is above that region's supplier average.

Links: ✓ "List" → shape `lookup`<br>✓ "names" → supplier.s_name<br>✓ "phone numbers" → supplier.s_phone<br>✓ "suppliers" → supplier<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "account balance" → supplier.s_acctbal<br>✓ "above that region's supplier average" → shape `vs_aggregate`

- Label check: tables:region confirmed, tables:supplier confirmed, columns:region.r_name confirmed, columns:supplier.s_acctbal confirmed, columns:supplier.s_name confirmed, columns:supplier.s_phone confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed, shapes:lookup not labeled
