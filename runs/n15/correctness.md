# Correctness report

- Generated: 2026-11-25T00:54:03+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n15/questions.json, questions_sha256=7dd977525fff7199a91884b99e7994c58661b8ed134cce569d73f8a60d4787ec, n=15, issues_accepted=0

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
| q01 | How did the total profit on items supplied by suppliers in FRANCE change year by year for shipments between 1993 and 1997? | **ANSWERABLE** | Profit is defined in the glossary (l_extendedprice*(1-l_discount) - ps_supplycost*l_quantity); suppliers in FRANCE via supplier.s_nationkey -> nation.n_name, grouped by year of lineitem.l_shipdate within 1993..1997. |
| q02 | Which 5 customers in INDIA placed the largest number of 1-URGENT orders in 1997? | **ANSWERABLE** | Count orders with orders.o_orderpriority = '1-URGENT' and o_orderdate in 1997 per customer whose nation (customer.c_nationkey -> nation.n_name) is INDIA, then take the top 5. |
| q03 | Which Brand#23 parts have no supplier located in the ASIA region? | **ANSWERABLE** | Parts with part.p_brand = 'Brand#23' for which no partsupp supplier sits in a nation of region.r_name = 'ASIA'; the glossary defines the part-supplier relationship through partsupp. |
| q04 | Which nations had a total order value from their customers in 1995 above the average across all nations? | **ANSWERABLE** | Order value is orders.o_totalprice (glossary); sum it per customer nation for o_orderdate in 1995 and keep nations whose total exceeds the mean of the per-nation totals. |
| q05 | Of the line items received in 1994 from suppliers in the AFRICA region, what fraction were returned? | **ANSWERABLE** | Among line items with lineitem.l_receiptdate in 1994 whose supplier's nation is in region AFRICA, the share with l_returnflag = 'R' (glossary: R = returned; all 1994 receipts predate 1995-06-17 so they carry R or A). |
| q06 | List the name, brand and retail price of every part of size 49 packed in an LG DRUM container. | **ANSWERABLE** | Direct lookup on part: p_name, p_brand, p_retailprice where p_size = 49 and p_container = 'LG DRUM'. |
| q07 | Which 5 suppliers hold the largest total available quantity of STEEL parts? | **ANSWERABLE** | Sum partsupp.ps_availqty per supplier over parts whose p_type material (last word, glossary: Part type) is STEEL, and take the top 5. |
| q08 | How did the number of line items shipped by FOB to customers in the MIDDLE EAST region change quarter by quarter in 1996? | **ANSWERABLE** | Count line items with lineitem.l_shipmode = 'FOB' and l_shipdate in 1996, for orders whose customer's nation is in region MIDDLE EAST, grouped by quarter of l_shipdate. |
| q09 | List the name and phone number of customers in the AUTOMOBILE segment in CANADA with a negative account balance. | **ANSWERABLE** | Lookup of customer.c_name and c_phone where c_mktsegment = 'AUTOMOBILE', nation.n_name = 'CANADA' and c_acctbal < 0. |
| q10 | What share of our suppliers' combined available quantity is held by suppliers with a negative account balance? | **ANSWERABLE** | Sum of partsupp.ps_availqty for suppliers with supplier.s_acctbal < 0 divided by the sum of ps_availqty over all suppliers. |
| q11 | Which suppliers in PERU had no line items with the shipping instruction COLLECT COD shipped last month? | **ANSWERABLE** | Suppliers with nation.n_name = 'PERU' having no line item with lineitem.l_shipinstruct = 'COLLECT COD' and l_shipdate in last month, which the time anchor resolves to 1998-07. |
| q12 | How many line items shipped in 1995 had a gross value above that year's average? | **ANSWERABLE** | Gross value is lineitem.l_extendedprice (glossary); count line items with l_shipdate in 1995 whose l_extendedprice exceeds the 1995 average of l_extendedprice. |
| q13 | What percentage of line items shipped by MAIL in 1996 were delivered late? | **ANSWERABLE** | Late delivery is l_receiptdate > l_commitdate (glossary); share of line items with l_shipmode = 'MAIL' and l_shipdate in 1996 that were late. |
| q14 | Which 10 clerks handled the highest total order value in 1996? | **ANSWERABLE** | Sum orders.o_totalprice (order value, glossary) per orders.o_clerk for o_orderdate in 1996 and take the top 10. |
| q15 | What is the phone number and account balance of Supplier#000000427? | **ANSWERABLE** | Direct lookup of supplier.s_phone and s_acctbal where s_name = 'Supplier#000000427'. |

## Evidence

### q01: ANSWERABLE

> How did the total profit on items supplied by suppliers in FRANCE change year by year for shipments between 1993 and 1997?

Links: ✓ "total" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "FRANCE" → nation.n_name = `FRANCE`<br>✓ "year by year" → shape `time_trend`<br>✓ "shipments between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`

- Label check: tables:lineitem confirmed, tables:nation confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:nation.n_name confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q02: ANSWERABLE

> Which 5 customers in INDIA placed the largest number of 1-URGENT orders in 1997?

Links: ✓ "5 customers" → customer<br>✓ "INDIA" → nation.n_name = `INDIA`<br>✓ "largest" → shape `ranking`<br>✓ "number of" → shape `aggregation`<br>✓ "1-URGENT" → orders.o_orderpriority = `1-URGENT`<br>✓ "orders in 1997" → orders.o_orderdate = `1997`

- Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q03: ANSWERABLE

> Which Brand#23 parts have no supplier located in the ASIA region?

Links: ✓ "Brand#23" → part.p_brand = `Brand#23`<br>✓ "parts" → part<br>✓ "have no supplier" → shape `anti_join`<br>✓ "supplier" → partsupp<br>✓ "supplier located" → supplier<br>✓ "ASIA region" → region.r_name = `ASIA`

- Label check: tables:part confirmed, tables:region confirmed, tables:supplier confirmed, tables:partsupp not labeled, columns:part.p_brand confirmed, columns:region.r_name confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q04: ANSWERABLE

> Which nations had a total order value from their customers in 1995 above the average across all nations?

Links: ✓ "nations" → nation<br>✓ "total" → shape `aggregation`<br>✓ "order value" → orders.o_totalprice<br>✓ "customers" → customer<br>✓ "in 1995" → orders.o_orderdate = `1995`<br>✓ "above the average across all nations" → shape `vs_aggregate`

- Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed

### q05: ANSWERABLE

> Of the line items received in 1994 from suppliers in the AFRICA region, what fraction were returned?

Links: ✓ "line items" → lineitem<br>✓ "received in 1994" → lineitem.l_receiptdate = `1994`<br>✓ "suppliers" → supplier<br>✓ "AFRICA region" → region.r_name = `AFRICA`<br>✓ "fraction" → shape `ratio`<br>✓ "returned" → lineitem.l_returnflag = `R`

- Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_returnflag confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q06: ANSWERABLE

> List the name, brand and retail price of every part of size 49 packed in an LG DRUM container.

Links: ✓ "List" → shape `lookup`<br>✓ "name" → part.p_name<br>✓ "brand" → part.p_brand<br>✓ "retail price" → part.p_retailprice<br>✓ "part" → part<br>✓ "size 49" → part.p_size = `49`<br>✓ "LG DRUM container" → part.p_container = `LG DRUM`

- Label check: tables:part confirmed, columns:part.p_brand confirmed, columns:part.p_container confirmed, columns:part.p_name confirmed, columns:part.p_retailprice confirmed, columns:part.p_size confirmed, shapes:lookup confirmed

### q07: ANSWERABLE

> Which 5 suppliers hold the largest total available quantity of STEEL parts?

Links: ✓ "5 suppliers" → supplier<br>✓ "largest" → shape `ranking`<br>✓ "total" → shape `aggregation`<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "STEEL parts" → part.p_type = `STEEL` (contains)

- Label check: tables:part confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:part.p_type confirmed, columns:partsupp.ps_availqty confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q08: ANSWERABLE

> How did the number of line items shipped by FOB to customers in the MIDDLE EAST region change quarter by quarter in 1996?

Links: ✓ "number of" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "shipped by FOB" → lineitem.l_shipmode = `FOB`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "quarter by quarter" → shape `time_trend`<br>✓ "shipped … in 1996" → lineitem.l_shipdate = `1996`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q09: ANSWERABLE

> List the name and phone number of customers in the AUTOMOBILE segment in CANADA with a negative account balance.

Links: ✓ "List" → shape `lookup`<br>✓ "name" → customer.c_name<br>✓ "phone number" → customer.c_phone<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "CANADA" → nation.n_name = `CANADA`<br>✓ "negative account balance" → customer.c_acctbal = `-999.95..-0.01`

- Label check: tables:customer confirmed, tables:nation confirmed, columns:customer.c_acctbal confirmed, columns:customer.c_mktsegment confirmed, columns:customer.c_name confirmed, columns:customer.c_phone confirmed, columns:nation.n_name confirmed, shapes:lookup confirmed

### q10: ANSWERABLE

> What share of our suppliers' combined available quantity is held by suppliers with a negative account balance?

Links: ✓ "share" → shape `ratio`<br>✓ "suppliers' combined available quantity" → partsupp.ps_availqty<br>✓ "combined" → shape `aggregation`<br>✓ "suppliers" → supplier<br>✓ "negative account balance" → supplier.s_acctbal = `-966.20..-0.01`

- Label check: tables:partsupp confirmed, tables:supplier confirmed, columns:partsupp.ps_availqty confirmed, columns:supplier.s_acctbal confirmed, shapes:ratio confirmed, shapes:aggregation not labeled

### q11: ANSWERABLE

> Which suppliers in PERU had no line items with the shipping instruction COLLECT COD shipped last month?

Links: ✓ "suppliers" → supplier<br>✓ "PERU" → nation.n_name = `PERU`<br>✓ "had no line items" → shape `anti_join`<br>✓ "line items" → lineitem<br>✓ "shipping instruction COLLECT COD" → lineitem.l_shipinstruct = `COLLECT COD`<br>✓ "shipped last month" → lineitem.l_shipdate = `1998-07`

- Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipinstruct confirmed, columns:nation.n_name confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q12: ANSWERABLE

> How many line items shipped in 1995 had a gross value above that year's average?

Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "shipped in 1995" → lineitem.l_shipdate = `1995`<br>✓ "gross value" → lineitem.l_extendedprice<br>✓ "above that year's average" → shape `vs_aggregate`

- Label check: tables:lineitem confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed

### q13: ANSWERABLE

> What percentage of line items shipped by MAIL in 1996 were delivered late?

Links: ✓ "percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "shipped by MAIL" → lineitem.l_shipmode = `MAIL`<br>✓ "in 1996" → lineitem.l_shipdate = `1996`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate

- Label check: tables:lineitem confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, shapes:ratio confirmed

### q14: ANSWERABLE

> Which 10 clerks handled the highest total order value in 1996?

Links: ✓ "10 clerks" → orders.o_clerk<br>✓ "highest" → shape `ranking`<br>✓ "total" → shape `aggregation`<br>✓ "order value" → orders.o_totalprice<br>✓ "in 1996" → orders.o_orderdate = `1996`

- Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:ranking confirmed

### q15: ANSWERABLE

> What is the phone number and account balance of Supplier#000000427?

Links: ✓ "What is" → shape `lookup`<br>✓ "phone number" → supplier.s_phone<br>✓ "account balance" → supplier.s_acctbal<br>✓ "Supplier#000000427" → supplier.s_name = `Supplier#000000427`

- Label check: tables:supplier confirmed, columns:supplier.s_acctbal confirmed, columns:supplier.s_name confirmed, columns:supplier.s_phone confirmed, shapes:lookup confirmed
