# Correctness report

- Generated: 2026-11-25T00:53:48+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n10/questions.json, questions_sha256=58cb94ab7968684aa10e493194ec4cd4bd55d22614369b4440634e4f57b68b40, n=10, issues_accepted=0

## Score

**1.0000** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (10 + 0.5 x 0) / 10 = 1.0000

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 0 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 10 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | Which 5 suppliers in RUSSIA earned the highest total profit on items shipped in 1996? | **ANSWERABLE** | Profit is defined in the glossary as l_extendedprice*(1-l_discount) - ps_supplycost*l_quantity; supplier nation via supplier.s_nationkey -> nation.n_name = RUSSIA, filtered on lineitem.l_shipdate in 1996 and ranked by summed profit. |
| q02 | How many MACHINERY customers in the ASIA region have never placed an order? | **ANSWERABLE** | Count customers with customer.c_mktsegment = MACHINERY whose nation is in region.r_name = ASIA and who have no row in orders (o_custkey); clause 1.4 notes a third of customers have no orders. |
| q03 | How did total revenue from Manufacturer#4 parts change year by year for items shipped between 1993 and 1997? | **ANSWERABLE** | Revenue is the glossary's l_extendedprice*(1-l_discount), restricted to part.p_mfgr = Manufacturer#4 and lineitem.l_shipdate in 1993..1997, grouped by ship year. |
| q04 | What proportion of line items received in 1995 from suppliers in the MIDDLE EAST region were delivered late? | **ANSWERABLE** | Late delivery is defined in the glossary as l_receiptdate > l_commitdate; the population is line items with l_receiptdate in 1995 whose supplier's nation is in region MIDDLE EAST, and the answer is late lines divided by all such lines. |
| q05 | Which regions generated more revenue from their customers' orders placed in 1997 than the average region? | **ANSWERABLE** | Revenue is the glossary's l_extendedprice*(1-l_discount) (distinct from order value), attributed to regions through the customer's nation, for orders with o_orderdate in 1997; regions whose total exceeds the mean of the five regional totals qualify. |
| q06 | List the clerk, order value and status of each 5-LOW priority order placed on 1 July 1998. | **ANSWERABLE** | Direct lookup on orders: o_clerk, o_totalprice (glossary: order value) and o_orderstatus for rows with o_orderpriority = 5-LOW and o_orderdate = 1998-07-01. |
| q07 | How did the total order value from customers in BRAZIL change quarter by quarter in 1997? | **ANSWERABLE** | Order value is o_totalprice per the glossary; sum it for customers whose nation is BRAZIL, for orders with o_orderdate in 1997, grouped by quarter of o_orderdate. |
| q08 | What percentage of the line items ordered by customers in KENYA during 1997 carried the shipping instruction COLLECT COD? | **ANSWERABLE** | Population: line items of orders with o_orderdate in 1997 placed by customers whose nation is KENYA; the answer is the share of those with lineitem.l_shipinstruct = COLLECT COD. |
| q09 | Which 5 parts packed in LG CASE containers brought in the highest total revenue from items shipped in 1996? | **ANSWERABLE** | Parts with part.p_container = LG CASE (a valid container per clause 4.2.2.13), ranked by summed glossary revenue l_extendedprice*(1-l_discount) over line items with l_shipdate in 1996. |
| q10 | Which nations have a mean supplier account balance higher than the average across all suppliers? | **ANSWERABLE** | Average supplier.s_acctbal per nation (via s_nationkey) compared with the overall average s_acctbal across all suppliers; the overall baseline is stated explicitly. |

## Evidence

### q01: ANSWERABLE

> Which 5 suppliers in RUSSIA earned the highest total profit on items shipped in 1996?

Links: ✓ "suppliers" → supplier<br>✓ "RUSSIA" → nation.n_name = `RUSSIA`<br>✓ "5 … highest" → shape `ranking`<br>✓ "total profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "total" → shape `aggregation`<br>✓ "shipped in 1996" → lineitem.l_shipdate = `1996`

- Label check: tables:lineitem confirmed, tables:nation confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:nation.n_name confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q02: ANSWERABLE

> How many MACHINERY customers in the ASIA region have never placed an order?

Links: ✓ "How many" → shape `aggregation`<br>✓ "MACHINERY" → customer.c_mktsegment = `MACHINERY`<br>✓ "customers" → customer<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "never" → shape `anti_join`<br>✓ "order" → orders

- Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:customer.c_mktsegment confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q03: ANSWERABLE

> How did total revenue from Manufacturer#4 parts change year by year for items shipped between 1993 and 1997?

Links: ✓ "total revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "total" → shape `aggregation`<br>✓ "Manufacturer#4" → part.p_mfgr = `Manufacturer#4`<br>✓ "parts" → part<br>✓ "year by year" → shape `time_trend`<br>✓ "shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`

- Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_mfgr confirmed, shapes:aggregation confirmed, shapes:time_trend confirmed

### q04: ANSWERABLE

> What proportion of line items received in 1995 from suppliers in the MIDDLE EAST region were delivered late?

Links: ✓ "proportion" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "received in 1995" → lineitem.l_receiptdate = `1995`<br>✓ "suppliers" → supplier<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate

- Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q05: ANSWERABLE

> Which regions generated more revenue from their customers' orders placed in 1997 than the average region?

Links: ✓ "regions" → region<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "customers'" → customer<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "more revenue … than the average region" → shape `vs_aggregate`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:orders confirmed, tables:region confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed

### q06: ANSWERABLE

> List the clerk, order value and status of each 5-LOW priority order placed on 1 July 1998.

Links: ✓ "List" → shape `lookup`<br>✓ "clerk" → orders.o_clerk<br>✓ "order value" → orders.o_totalprice<br>✓ "status" → orders.o_orderstatus<br>✓ "5-LOW priority" → orders.o_orderpriority = `5-LOW`<br>✓ "order placed on 1 July 1998" → orders.o_orderdate = `1998-07-01`<br>✓ "order" → orders

- Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, columns:orders.o_orderstatus confirmed, columns:orders.o_totalprice confirmed, shapes:lookup confirmed

### q07: ANSWERABLE

> How did the total order value from customers in BRAZIL change quarter by quarter in 1997?

Links: ✓ "total order value" → orders.o_totalprice<br>✓ "total" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "BRAZIL" → nation.n_name = `BRAZIL`<br>✓ "quarter by quarter" → shape `time_trend`<br>✓ "in 1997" → orders.o_orderdate = `1997`

- Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q08: ANSWERABLE

> What percentage of the line items ordered by customers in KENYA during 1997 carried the shipping instruction COLLECT COD?

Links: ✓ "percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "ordered … during 1997" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "KENYA" → nation.n_name = `KENYA`<br>✓ "shipping instruction COLLECT COD" → lineitem.l_shipinstruct = `COLLECT COD`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_shipinstruct confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q09: ANSWERABLE

> Which 5 parts packed in LG CASE containers brought in the highest total revenue from items shipped in 1996?

Links: ✓ "parts" → part<br>✓ "LG CASE containers" → part.p_container = `LG CASE`<br>✓ "5 … highest" → shape `ranking`<br>✓ "total revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "total" → shape `aggregation`<br>✓ "items shipped in 1996" → lineitem.l_shipdate = `1996`

- Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_container confirmed, shapes:aggregation confirmed, shapes:ranking confirmed

### q10: ANSWERABLE

> Which nations have a mean supplier account balance higher than the average across all suppliers?

Links: ✓ "nations" → nation<br>✓ "mean" → shape `aggregation`<br>✓ "supplier account balance" → supplier.s_acctbal<br>✓ "higher than the average across all suppliers" → shape `vs_aggregate`

- Label check: tables:nation confirmed, tables:supplier confirmed, columns:supplier.s_acctbal confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed
