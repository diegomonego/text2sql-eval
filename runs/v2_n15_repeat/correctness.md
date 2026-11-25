# Correctness report

- Generated: 2026-11-25T14:48:51+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 8336fc3a2fd163ba4c9a16399c054d17e9393a68
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/v2_n15_repeat/questions.json, questions_sha256=62bc445cf9e8903d2edb2ed42f203e75c8c008c8178e24e27de74d79c17c07b7, n=15, issues_accepted=0

## Score

**1.0000** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (15 + 0.5 x 0) / 15 = 1.0000

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 0 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 15 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | How did the average line item discount for customers in the UNITED KINGDOM change by year for orders placed between 1992 and 1997? | **ANSWERABLE** | Average of lineitem.l_discount per year of orders.o_orderdate (1992..1997), restricted to customers whose nation.n_name is UNITED KINGDOM via customer.c_nationkey. 'By year' follows the stated order-date filter, and the customer's nation is named explicitly, so there is one reading. |
| q02 | List the name, supply cost and available quantity of every part offered by Supplier#000000137. | **ANSWERABLE** | Lookup of part.p_name, partsupp.ps_supplycost and partsupp.ps_availqty for the partsupp rows of the supplier whose supplier.s_name is Supplier#000000137. 'Name' attaches to 'part', so it is the part name, not the supplier's. |
| q03 | How many parts have never been sold to customers in the EUROPE region? | **ANSWERABLE** | Count of parts in the part table with no lineitem on an order from a customer whose nation is in region.r_name EUROPE. The question names the customers' region explicitly, which rules out a supplier-region reading. |
| q04 | For customers in the MIDDLE EAST region, what percentage of line items shipped in 1997 went by AIR? | **ANSWERABLE** | Share of line items with lineitem.l_shipmode = 'AIR' among line items with l_shipdate in 1997 on orders from MIDDLE EAST customers (region.r_name). 'Percentage of line items' means a count of lines, not their value. 'AIR' matches the stored code exactly, so the reading that also counts 'REG AIR' is rejected. |
| q05 | Which 5 nations had the highest total charge, including tax, on orders their customers placed in 1996? | **ANSWERABLE** | Top 5 customer nations by total charge (glossary: l_extendedprice*(1-l_discount)*(1+l_tax)) on orders with o_orderdate in 1996. Summing orders.o_totalprice instead gives the same total, because spec 4.2.3 defines it as the sum of these charges, so the stored and computed routes agree. |
| q06 | Which nations have an average customer account balance above the average across all customers? | **ANSWERABLE** | Nations (via customer.c_nationkey) whose mean customer.c_acctbal is above the mean c_acctbal of all customers. 'Across all customers' settles that the benchmark is the overall customer average, not an average of nation averages, and needs no join to orders. |
| q07 | How did the average shipping time to customers in the ASIA region change by year for line items shipped between 1993 and 1997? | **ANSWERABLE** | Average shipping time (glossary: l_receiptdate - l_shipdate) per year of lineitem.l_shipdate for 1993..1997, for lines on orders from customers in region.r_name ASIA. The glossary defines shipping time, and grouping by ship year follows the stated ship-date filter. |
| q08 | List the order value, clerk and status of every 1-URGENT order placed on 1998-08-02. | **ANSWERABLE** | Lookup of orders.o_totalprice (glossary: order value), o_clerk and o_orderstatus for orders with o_orderpriority '1-URGENT' and o_orderdate 1998-08-02. 'Status of every … order' means the order status, not the line status. |
| q09 | What percentage of suppliers have a negative account balance? | **ANSWERABLE** | Share of supplier rows with supplier.s_acctbal < 0 out of all suppliers. Only one table and one column are involved. |
| q10 | How many orders placed in 1994 had no returned line items? | **ANSWERABLE** | Count of orders with o_orderdate in 1994 that have no line with lineitem.l_returnflag = 'R' (glossary: R = returned). Every 1994 line was received before 1995-06-17, so each one carries R or A and none is 'not yet received'. |
| q11 | Which 5 parts in LG CASE containers have the highest retail price? | **ANSWERABLE** | Top 5 parts by part.p_retailprice among parts with p_container = 'LG CASE'. All the data is in the part table. |
| q12 | How many supplier offers for Brand#33 parts have a supply cost above the average supply cost for the same part? | **ANSWERABLE** | Count of partsupp rows for parts with part.p_brand = 'Brand#33' whose ps_supplycost exceeds the average ps_supplycost over that part's partsupp rows. 'For the same part' fixes the comparison group. |
| q13 | How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997? | **ANSWERABLE** | Count of orders per year of orders.o_orderdate (1993..1997) for customers with customer.c_mktsegment = 'AUTOMOBILE'. Orders carry only one date, so the year has a single meaning. |
| q14 | List the quantity, ship mode and shipping instruction of every line item shipped on 1998-12-01. | **ANSWERABLE** | Lookup of lineitem.l_quantity, l_shipmode and l_shipinstruct for lines with l_shipdate = 1998-12-01, which is inside the data's ship-date range. 'Shipped on' names the ship date explicitly. |
| q15 | What share of revenue from orders placed in 1997 came from customers in CHINA? | **ANSWERABLE** | Revenue (glossary: l_extendedprice*(1-l_discount)) from customers whose nation.n_name is CHINA, divided by total revenue, over orders with o_orderdate in 1997. The glossary defines revenue, and the customer's nation is named explicitly. |

## Evidence

### q01: ANSWERABLE

> How did the average line item discount for customers in the UNITED KINGDOM change by year for orders placed between 1992 and 1997?

Links: ✓ "average" → shape `aggregation`<br>✓ "line item discount" → lineitem.l_discount<br>✓ "customers" → customer<br>✓ "UNITED KINGDOM" → nation.n_name = `UNITED KINGDOM`<br>✓ "change by year" → shape `time_trend`<br>✓ "orders placed between 1992 and 1997" → orders.o_orderdate = `1992..1997`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q02: ANSWERABLE

> List the name, supply cost and available quantity of every part offered by Supplier#000000137.

Links: ✓ "List" → shape `lookup`<br>✓ "name" → part.p_name<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "part" → part<br>✓ "offered by" → partsupp<br>✓ "Supplier#000000137" → supplier.s_name = `Supplier#000000137`

- Label check: tables:part confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:part.p_name confirmed, columns:partsupp.ps_availqty confirmed, columns:partsupp.ps_supplycost confirmed, columns:supplier.s_name confirmed, shapes:lookup confirmed, shapes:multi_join confirmed

### q03: ANSWERABLE

> How many parts have never been sold to customers in the EUROPE region?

Links: ✓ "How many" → shape `aggregation`<br>✓ "parts" → part<br>✓ "never" → shape `anti_join`<br>✓ "sold" → lineitem<br>✓ "customers" → customer<br>✓ "EUROPE region" → region.r_name = `EUROPE`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:part confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q04: ANSWERABLE

> For customers in the MIDDLE EAST region, what percentage of line items shipped in 1997 went by AIR?

Links: ✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "shipped in 1997" → lineitem.l_shipdate = `1997`<br>✓ "went by AIR" → lineitem.l_shipmode = `AIR`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q05: ANSWERABLE

> Which 5 nations had the highest total charge, including tax, on orders their customers placed in 1996?

Links: ✓ "nations" → nation<br>✓ "highest" → shape `ranking`<br>✓ "total" → shape `aggregation`<br>✓ "charge, including tax" → lineitem.l_extendedprice, lineitem.l_discount, lineitem.l_tax<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "placed in 1996" → orders.o_orderdate = `1996`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_tax confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q06: ANSWERABLE

> Which nations have an average customer account balance above the average across all customers?

Links: ✓ "nations" → nation<br>✓ "average" → shape `aggregation`<br>✓ "customer account balance" → customer.c_acctbal<br>✓ "above the average across all customers" → shape `vs_aggregate`

- Label check: tables:customer confirmed, tables:nation confirmed, columns:customer.c_acctbal confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed

### q07: ANSWERABLE

> How did the average shipping time to customers in the ASIA region change by year for line items shipped between 1993 and 1997?

Links: ✓ "average" → shape `aggregation`<br>✓ "shipping time" → lineitem.l_receiptdate, lineitem.l_shipdate<br>✓ "customers" → customer<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "change by year" → shape `time_trend`<br>✓ "line items" → lineitem<br>✓ "shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`

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

Links: ✓ "parts" → part<br>✓ "LG CASE containers" → part.p_container = `LG CASE`<br>✓ "highest" → shape `ranking`<br>✓ "retail price" → part.p_retailprice

- Label check: tables:part confirmed, columns:part.p_container confirmed, columns:part.p_retailprice confirmed, shapes:ranking confirmed

### q12: ANSWERABLE

> How many supplier offers for Brand#33 parts have a supply cost above the average supply cost for the same part?

Links: ✓ "How many" → shape `aggregation`<br>✓ "supplier offers" → partsupp<br>✓ "Brand#33" → part.p_brand = `Brand#33`<br>✓ "parts" → part<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "above the average supply cost for the same part" → shape `vs_aggregate`

- Label check: tables:part confirmed, tables:partsupp confirmed, columns:part.p_brand confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed

### q13: ANSWERABLE

> How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997?

Links: ✓ "number of" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "year by year" → shape `time_trend`<br>✓ "between 1993 and 1997" → orders.o_orderdate = `1993..1997`

- Label check: tables:customer confirmed, tables:orders confirmed, columns:customer.c_mktsegment confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:time_trend confirmed

### q14: ANSWERABLE

> List the quantity, ship mode and shipping instruction of every line item shipped on 1998-12-01.

Links: ✓ "List" → shape `lookup`<br>✓ "quantity" → lineitem.l_quantity<br>✓ "ship mode" → lineitem.l_shipmode<br>✓ "shipping instruction" → lineitem.l_shipinstruct<br>✓ "line item" → lineitem<br>✓ "shipped on 1998-12-01" → lineitem.l_shipdate = `1998-12-01`

- Label check: tables:lineitem confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipinstruct confirmed, columns:lineitem.l_shipmode confirmed, shapes:lookup confirmed

### q15: ANSWERABLE

> What share of revenue from orders placed in 1997 came from customers in CHINA?

Links: ✓ "share" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "CHINA" → nation.n_name = `CHINA`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
