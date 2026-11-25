# Correctness report

- Generated: 2026-11-25T14:53:28+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 7cd82794b736dc1a0b94a142382d6c4310cd0cbb
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/v2_n15_controlled/questions.json, questions_sha256=5de8f71dc33cc7a761d5af59c091674336ff6f62a76f9227fba5c2ff507986ae, n=15, issues_accepted=0

## Score

**0.9333** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (14 + 0.5 x 0) / 15 = 0.9333

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 1 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 14 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | How did the average line item discount for customers in the UNITED KINGDOM change by year for orders placed between 1992 and 1997? | **ANSWERABLE** | Average of lineitem.l_discount per year of orders.o_orderdate (1992..1997), for lines on orders whose customer's nation (customer.c_nationkey -> nation.n_name) is UNITED KINGDOM. A price-weighted discount is a less natural reading of 'average line item discount' and was rejected. |
| q02 | List the name, supply cost and available quantity of every part offered by Supplier#000000137. | **ANSWERABLE** | Lookup on partsupp for the supplier with s_name Supplier#000000137, returning part.p_name, partsupp.ps_supplycost and partsupp.ps_availqty. 'name' attaches to 'every part', so it is the part name, not the supplier name. |
| q03 | How many parts have never been sold to customers in the EUROPE region? | **ANSWERABLE** | Count parts with no lineitem row on an order whose customer's region (customer -> nation -> region.r_name) is EUROPE. The question names the customers' region explicitly, so the supplier's region is not a competing reading; 'sold' means appearing in lineitem. |
| q04 | How many orders were cancelled in 1997? | **MISSING_DATA** | No column records cancellations: orders.o_orderstatus is F/O/P (fulfilled, open, partially fulfilled per the glossary) and lineitem.l_returnflag records returns, not cancellations. |
| q05 | Which 5 nations had the highest total charge, including tax, on orders their customers placed in 1996? | **ANSWERABLE** | Top 5 customer nations by summed charge (glossary: l_extendedprice x (1 - l_discount) x (1 + l_tax)) on orders with o_orderdate in 1996. Summing orders.o_totalprice gives the same result since the spec defines it as the sum of the line charges, so stored vs computed is not a material difference. |
| q06 | Which nations have an average customer account balance above the average across all customers? | **ANSWERABLE** | Per nation, average customer.c_acctbal, compared with the mean c_acctbal over all customers. 'across all customers' rules out the average of nation averages. |
| q07 | How did the average shipping time to customers in the ASIA region change by year for line items shipped between 1993 and 1997? | **ANSWERABLE** | Shipping time is defined in the glossary as l_receiptdate - l_shipdate; average it per year of l_shipdate (1993..1997) for lines on orders of customers in region ASIA. Grouping by order year was considered, but the only period named is the ship date. |
| q08 | List the order value, clerk and status of every 1-URGENT order placed on 1998-08-02. | **ANSWERABLE** | Lookup on orders with o_orderpriority = 1-URGENT and o_orderdate = 1998-08-02, returning o_totalprice (glossary: order value), o_clerk and o_orderstatus. |
| q09 | What percentage of suppliers have a negative account balance? | **ANSWERABLE** | Share of supplier rows with supplier.s_acctbal < 0 over all suppliers; the glossary notes balances can be negative. |
| q10 | How many orders placed in 1994 had no returned line items? | **ANSWERABLE** | Count orders with o_orderdate in 1994 that have no lineitem with l_returnflag = 'R' (glossary: R = returned). All 1994 lines are received before 1995-06-17, so the N code does not blur the population. |
| q11 | Which 5 parts in LG CASE containers have the highest retail price? | **ANSWERABLE** | Top 5 parts with p_container = 'LG CASE' by part.p_retailprice. The glossary ties retail price to the part (l_extendedprice is quantity x retail price), so there is no competing column. |
| q12 | How many supplier offers for Brand#33 parts have a supply cost above the average supply cost for the same part? | **ANSWERABLE** | Count partsupp rows for parts with p_brand = Brand#33 whose ps_supplycost exceeds the average ps_supplycost of that same ps_partkey. |
| q13 | How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997? | **ANSWERABLE** | Count of orders per year of o_orderdate (1993..1997) for customers with c_mktsegment = AUTOMOBILE; o_orderdate is the only order-level date. |
| q14 | List the quantity, ship mode and shipping instruction of every line item shipped on 1998-12-01. | **ANSWERABLE** | Lookup on lineitem with l_shipdate = 1998-12-01 (the latest ship date in the data), returning l_quantity, l_shipmode and l_shipinstruct. |
| q15 | Between 1993 and 1997, how many orders did customers in the AUTOMOBILE segment place each year? | **ANSWERABLE** | Count of orders per year of o_orderdate (1993..1997) placed by customers with c_mktsegment = AUTOMOBILE. |

## Evidence

### q01: ANSWERABLE

> How did the average line item discount for customers in the UNITED KINGDOM change by year for orders placed between 1992 and 1997?

Links: ✓ "change by year" → shape `time_trend`<br>✓ "average" → shape `aggregation`<br>✓ "line item discount" → lineitem.l_discount<br>✓ "customers" → customer<br>✓ "UNITED KINGDOM" → nation.n_name = `UNITED KINGDOM`<br>✓ "orders placed between 1992 and 1997" → orders.o_orderdate = `1992..1997`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q02: ANSWERABLE

> List the name, supply cost and available quantity of every part offered by Supplier#000000137.

Links: ✓ "List" → shape `lookup`<br>✓ "name" → part.p_name<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "part offered by" → partsupp<br>✓ "Supplier#000000137" → supplier.s_name = `Supplier#000000137`

- Label check: tables:part confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:part.p_name confirmed, columns:partsupp.ps_availqty confirmed, columns:partsupp.ps_supplycost confirmed, columns:supplier.s_name confirmed, shapes:lookup confirmed, shapes:multi_join confirmed

### q03: ANSWERABLE

> How many parts have never been sold to customers in the EUROPE region?

Links: ✓ "How many" → shape `aggregation`<br>✓ "parts" → part<br>✓ "never" → shape `anti_join`<br>✓ "sold" → lineitem<br>✓ "customers" → customer<br>✓ "EUROPE region" → region.r_name = `EUROPE`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:part confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q04: MISSING_DATA

> How many orders were cancelled in 1997?

Links: ✓ "How many" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "cancelled" → MISSING: order cancellation<br>✓ "in 1997" → orders.o_orderdate = `1997`

- Missing concept: **order cancellation**. Closest: orders.o_orderstatus, lineitem.l_returnflag. o_orderstatus only codes fulfilled/open/partial and l_returnflag codes returns; no cancellation status exists

### q05: ANSWERABLE

> Which 5 nations had the highest total charge, including tax, on orders their customers placed in 1996?

Links: ✓ "Which 5 … highest" → shape `ranking`<br>✓ "nations" → nation<br>✓ "total" → shape `aggregation`<br>✓ "charge, including tax" → lineitem.l_extendedprice, lineitem.l_discount, lineitem.l_tax<br>✓ "customers" → customer<br>✓ "placed in 1996" → orders.o_orderdate = `1996`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_tax confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q06: ANSWERABLE

> Which nations have an average customer account balance above the average across all customers?

Links: ✓ "nations" → nation<br>✓ "average customer account balance" → customer.c_acctbal<br>✓ "average" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "above the average across all customers" → shape `vs_aggregate`

- Label check: tables:customer confirmed, tables:nation confirmed, columns:customer.c_acctbal confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed

### q07: ANSWERABLE

> How did the average shipping time to customers in the ASIA region change by year for line items shipped between 1993 and 1997?

Links: ✓ "change by year" → shape `time_trend`<br>✓ "average" → shape `aggregation`<br>✓ "shipping time" → lineitem.l_receiptdate, lineitem.l_shipdate<br>✓ "customers" → customer<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "line items shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_shipdate confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q08: ANSWERABLE

> List the order value, clerk and status of every 1-URGENT order placed on 1998-08-02.

Links: ✓ "List" → shape `lookup`<br>✓ "order value" → orders.o_totalprice<br>✓ "clerk" → orders.o_clerk<br>✓ "status" → orders.o_orderstatus<br>✓ "1-URGENT" → orders.o_orderpriority = `1-URGENT`<br>✓ "placed on 1998-08-02" → orders.o_orderdate = `1998-08-02`

- Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, columns:orders.o_orderstatus confirmed, columns:orders.o_totalprice confirmed, shapes:lookup confirmed

### q09: ANSWERABLE

> What percentage of suppliers have a negative account balance?

Links: ✓ "percentage" → shape `ratio`<br>✓ "suppliers" → supplier<br>✓ "negative account balance" → supplier.s_acctbal

- Label check: tables:supplier confirmed, columns:supplier.s_acctbal confirmed, shapes:ratio confirmed

### q10: ANSWERABLE

> How many orders placed in 1994 had no returned line items?

Links: ✓ "How many" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "placed in 1994" → orders.o_orderdate = `1994`<br>✓ "had no" → shape `anti_join`<br>✓ "returned line items" → lineitem.l_returnflag = `R`

- Label check: tables:lineitem confirmed, tables:orders confirmed, columns:lineitem.l_returnflag confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed

### q11: ANSWERABLE

> Which 5 parts in LG CASE containers have the highest retail price?

Links: ✓ "Which 5 … highest" → shape `ranking`<br>✓ "parts" → part<br>✓ "LG CASE containers" → part.p_container = `LG CASE`<br>✓ "retail price" → part.p_retailprice

- Label check: tables:part confirmed, columns:part.p_container confirmed, columns:part.p_retailprice confirmed, shapes:ranking confirmed

### q12: ANSWERABLE

> How many supplier offers for Brand#33 parts have a supply cost above the average supply cost for the same part?

Links: ✓ "How many" → shape `aggregation`<br>✓ "supplier offers" → partsupp<br>✓ "Brand#33" → part.p_brand = `Brand#33`<br>✓ "parts" → part<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "above the average supply cost for the same part" → shape `vs_aggregate`

- Label check: tables:part confirmed, tables:partsupp confirmed, columns:part.p_brand confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed

### q13: ANSWERABLE

> How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997?

Links: ✓ "number of orders" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "change year by year" → shape `time_trend`<br>✓ "between 1993 and 1997" → orders.o_orderdate = `1993..1997`

- Label check: tables:customer confirmed, tables:orders confirmed, columns:customer.c_mktsegment confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:time_trend confirmed

### q14: ANSWERABLE

> List the quantity, ship mode and shipping instruction of every line item shipped on 1998-12-01.

Links: ✓ "List" → shape `lookup`<br>✓ "quantity" → lineitem.l_quantity<br>✓ "ship mode" → lineitem.l_shipmode<br>✓ "shipping instruction" → lineitem.l_shipinstruct<br>✓ "line item" → lineitem<br>✓ "shipped on 1998-12-01" → lineitem.l_shipdate = `1998-12-01`

- Label check: tables:lineitem confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipinstruct confirmed, columns:lineitem.l_shipmode confirmed, shapes:lookup confirmed

### q15: ANSWERABLE

> Between 1993 and 1997, how many orders did customers in the AUTOMOBILE segment place each year?

Links: ✓ "Between 1993 and 1997" → orders.o_orderdate = `1993..1997`<br>✓ "how many orders" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "each year" → shape `time_trend`

