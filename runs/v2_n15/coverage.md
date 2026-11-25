# Coverage report

- Generated: 2026-11-25T14:47:01+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 8336fc3a2fd163ba4c9a16399c054d17e9393a68
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/v2_n15/questions.json, questions_sha256=62bc445cf9e8903d2edb2ed42f203e75c8c008c8178e24e27de74d79c17c07b7, n=15, issues_accepted=0

## Coverage by dimension

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 8 | 8 | 100.0 |
| columns | 26 | 61 | 42.62 |
| shapes | 8 | 8 | 100.0 |

- **Uncovered tables (0):** none
- **Uncovered columns (35):** **customer**: `c_custkey`, `c_name`, `c_address`, `c_nationkey`, `c_phone`, `c_comment`; **lineitem**: `l_orderkey`, `l_partkey`, `l_suppkey`, `l_linenumber`, `l_linestatus`, `l_commitdate`, `l_comment`; **nation**: `n_nationkey`, `n_regionkey`, `n_comment`; **orders**: `o_orderkey`, `o_custkey`, `o_shippriority` (constant in this data), `o_comment`; **part**: `p_partkey`, `p_mfgr`, `p_type`, `p_size`, `p_comment`; **partsupp**: `ps_partkey`, `ps_suppkey`, `ps_comment`; **region**: `r_regionkey`, `r_comment`; **supplier**: `s_suppkey`, `s_address`, `s_nationkey`, `s_phone`, `s_comment`
- **Uncovered shapes (0):** none

## Budget

N = 15. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 2.7 columns on average, so even with no repetition at most about 41 of 61 columns (67%) could be covered at this N; 26 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Which questions cover each item

### Tables

| item | covered by |
|---|---|
| `customer` | q01, q03, q04, q05, q06, q07, q13, q15 |
| `lineitem` | q01, q03, q04, q05, q07, q10, q14, q15 |
| `nation` | q01, q05, q06, q15 |
| `orders` | q01, q05, q08, q10, q13, q15 |
| `part` | q02, q03, q11, q12 |
| `partsupp` | q02, q12 |
| `region` | q03, q04, q07 |
| `supplier` | q02, q09 |

### Columns

| item | covered by |
|---|---|
| `customer.c_acctbal` | q06 |
| `customer.c_mktsegment` | q13 |
| `lineitem.l_quantity` | q14 |
| `lineitem.l_extendedprice` | q05, q15 |
| `lineitem.l_discount` | q01, q05, q15 |
| `lineitem.l_tax` | q05 |
| `lineitem.l_returnflag` | q10 |
| `lineitem.l_shipdate` | q04, q07, q14 |
| `lineitem.l_receiptdate` | q07 |
| `lineitem.l_shipinstruct` | q14 |
| `lineitem.l_shipmode` | q04, q14 |
| `nation.n_name` | q01, q15 |
| `orders.o_orderstatus` | q08 |
| `orders.o_totalprice` | q08 |
| `orders.o_orderdate` | q01, q05, q08, q10, q13, q15 |
| `orders.o_orderpriority` | q08 |
| `orders.o_clerk` | q08 |
| `part.p_name` | q02 |
| `part.p_brand` | q12 |
| `part.p_container` | q11 |
| `part.p_retailprice` | q11 |
| `partsupp.ps_availqty` | q02 |
| `partsupp.ps_supplycost` | q02, q12 |
| `region.r_name` | q03, q04, q07 |
| `supplier.s_name` | q02 |
| `supplier.s_acctbal` | q09 |

### Shapes

| item | covered by |
|---|---|
| `lookup` | q02, q08, q14 |
| `aggregation` | q01, q03, q05, q06, q07, q10, q12, q13 |
| `multi_join` | q01, q02, q03, q04, q05, q07, q15 |
| `ranking` | q05, q11 |
| `time_trend` | q01, q07, q13 |
| `ratio` | q04, q09, q15 |
| `vs_aggregate` | q06, q12 |
| `anti_join` | q03, q10 |

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: q01, q03, q04, q15
- Questions earning no credit: none

## Summary score

**80.87** = (table % + column % + shape %) / 3 = (100.0 + 42.62 + 100.0) / 3 = 80.87

The three dimensions above, weighted equally. Tables and shapes fill up within a few questions, so at small N this number mostly tracks column coverage. Read the dimensions first.

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | How did the average line item discount for customers in the UNITED KINGDOM change by year for orders placed between 1992 and 1997? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, nation.n_name, orders.o_orderdate; shapes: aggregation, multi_join, time_trend | nothing | - |
| q02 | List the name, supply cost and available quantity of every part offered by Supplier#000000137. | tables: part, partsupp, supplier; columns: part.p_name, partsupp.ps_availqty, partsupp.ps_supplycost, supplier.s_name; shapes: lookup, multi_join | columns:part.p_name, columns:partsupp.ps_availqty, columns:supplier.s_name | - |
| q03 | How many parts have never been sold to customers in the EUROPE region? | tables: customer, lineitem, part, region; columns: region.r_name; shapes: aggregation, anti_join, multi_join | nothing | - |
| q04 | For customers in the MIDDLE EAST region, what percentage of line items shipped in 1997 went by AIR? | tables: customer, lineitem, region; columns: lineitem.l_shipdate, lineitem.l_shipmode, region.r_name; shapes: multi_join, ratio | nothing | - |
| q05 | Which 5 nations had the highest total charge, including tax, on orders their customers placed in 1996? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_tax, orders.o_orderdate; shapes: aggregation, multi_join, ranking | columns:lineitem.l_tax | - |
| q06 | Which nations have an average customer account balance above the average across all customers? | tables: customer, nation; columns: customer.c_acctbal; shapes: aggregation, vs_aggregate | columns:customer.c_acctbal | - |
| q07 | How did the average shipping time to customers in the ASIA region change by year for line items shipped between 1993 and 1997? | tables: customer, lineitem, region; columns: lineitem.l_receiptdate, lineitem.l_shipdate, region.r_name; shapes: aggregation, multi_join, time_trend | columns:lineitem.l_receiptdate | - |
| q08 | List the order value, clerk and status of every 1-URGENT order placed on 1998-08-02. | tables: orders; columns: orders.o_clerk, orders.o_orderdate, orders.o_orderpriority, orders.o_orderstatus, orders.o_totalprice; shapes: lookup | columns:orders.o_clerk, columns:orders.o_orderpriority, columns:orders.o_orderstatus, columns:orders.o_totalprice | - |
| q09 | What percentage of suppliers have a negative account balance? | tables: supplier; columns: supplier.s_acctbal; shapes: ratio | columns:supplier.s_acctbal | - |
| q10 | How many orders placed in 1994 had no returned line items? | tables: lineitem, orders; columns: lineitem.l_returnflag, orders.o_orderdate; shapes: aggregation, anti_join | columns:lineitem.l_returnflag | - |
| q11 | Which 5 parts in LG CASE containers have the highest retail price? | tables: part; columns: part.p_container, part.p_retailprice; shapes: ranking | columns:part.p_container, columns:part.p_retailprice | - |
| q12 | How many supplier offers for Brand#33 parts have a supply cost above the average supply cost for the same part? | tables: part, partsupp; columns: part.p_brand, partsupp.ps_supplycost; shapes: aggregation, vs_aggregate | columns:part.p_brand | - |
| q13 | How did the number of orders from customers in the AUTOMOBILE segment change year by year between 1993 and 1997? | tables: customer, orders; columns: customer.c_mktsegment, orders.o_orderdate; shapes: aggregation, time_trend | columns:customer.c_mktsegment | - |
| q14 | List the quantity, ship mode and shipping instruction of every line item shipped on 1998-12-01. | tables: lineitem; columns: lineitem.l_quantity, lineitem.l_shipdate, lineitem.l_shipinstruct, lineitem.l_shipmode; shapes: lookup | columns:lineitem.l_quantity, columns:lineitem.l_shipinstruct | - |
| q15 | What share of revenue from orders placed in 1997 came from customers in CHINA? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, lineitem.l_extendedprice, nation.n_name, orders.o_orderdate; shapes: multi_join, ratio | nothing | - |

## Links

- **q01**: ✓ "average" → shape `aggregation`<br>✓ "line item discount" → lineitem.l_discount<br>✓ "customers" → customer<br>✓ "UNITED KINGDOM" → nation.n_name = `UNITED KINGDOM`<br>✓ "change by year" → shape `time_trend`<br>✓ "orders placed between 1992 and 1997" → orders.o_orderdate = `1992..1997`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q02**: ✓ "List" → shape `lookup`<br>✓ "name" → part.p_name<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "part" → part<br>✓ "offered" → partsupp<br>✓ "Supplier#000000137" → supplier.s_name = `Supplier#000000137`
  - Label check: tables:part confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:part.p_name confirmed, columns:partsupp.ps_availqty confirmed, columns:partsupp.ps_supplycost confirmed, columns:supplier.s_name confirmed, shapes:lookup confirmed, shapes:multi_join confirmed
- **q03**: ✓ "How many" → shape `aggregation`<br>✓ "parts" → part<br>✓ "never" → shape `anti_join`<br>✓ "sold" → lineitem<br>✓ "customers" → customer<br>✓ "EUROPE region" → region.r_name = `EUROPE`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:part confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q04**: ✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "shipped in 1997" → lineitem.l_shipdate = `1997`<br>✓ "went by AIR" → lineitem.l_shipmode = `AIR`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q05**: ✓ "5 nations had the highest" → shape `ranking`<br>✓ "nations" → nation<br>✓ "total" → shape `aggregation`<br>✓ "total charge, including tax" → lineitem.l_extendedprice, lineitem.l_discount, lineitem.l_tax<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "placed in 1996" → orders.o_orderdate = `1996`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_tax confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed
- **q06**: ✓ "nations" → nation<br>✓ "average customer account balance" → customer.c_acctbal<br>✓ "average customer account balance" → shape `aggregation`<br>✓ "above the average across all customers" → shape `vs_aggregate`<br>✓ "customers" → customer
  - Label check: tables:customer confirmed, tables:nation confirmed, columns:customer.c_acctbal confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed
- **q07**: ✓ "average" → shape `aggregation`<br>✓ "shipping time" → lineitem.l_receiptdate, lineitem.l_shipdate<br>✓ "customers" → customer<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "change by year" → shape `time_trend`<br>✓ "line items shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_shipdate confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q08**: ✓ "List" → shape `lookup`<br>✓ "order value" → orders.o_totalprice<br>✓ "clerk" → orders.o_clerk<br>✓ "status" → orders.o_orderstatus<br>✓ "1-URGENT" → orders.o_orderpriority = `1-URGENT`<br>✓ "order placed on 1998-08-02" → orders.o_orderdate = `1998-08-02`
  - Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, columns:orders.o_orderstatus confirmed, columns:orders.o_totalprice confirmed, shapes:lookup confirmed
- **q09**: ✓ "percentage" → shape `ratio`<br>✓ "suppliers" → supplier<br>✓ "negative account balance" → supplier.s_acctbal
  - Label check: tables:supplier confirmed, columns:supplier.s_acctbal confirmed, shapes:ratio confirmed
- **q10**: ✓ "How many" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "placed in 1994" → orders.o_orderdate = `1994`<br>✓ "had no returned line items" → shape `anti_join`<br>✓ "returned" → lineitem.l_returnflag = `R`<br>✓ "line items" → lineitem
  - Label check: tables:lineitem confirmed, tables:orders confirmed, columns:lineitem.l_returnflag confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed
- **q11**: ✓ "5 parts" → shape `ranking`<br>✓ "highest" → shape `ranking`<br>✓ "parts" → part<br>✓ "LG CASE containers" → part.p_container = `LG CASE`<br>✓ "retail price" → part.p_retailprice
  - Label check: tables:part confirmed, columns:part.p_container confirmed, columns:part.p_retailprice confirmed, shapes:ranking confirmed
- **q12**: ✓ "How many" → shape `aggregation`<br>✓ "supplier offers" → partsupp<br>✓ "Brand#33" → part.p_brand = `Brand#33`<br>✓ "parts" → part<br>✓ "supply cost" → partsupp.ps_supplycost<br>✓ "above the average supply cost for the same part" → shape `vs_aggregate`
  - Label check: tables:part confirmed, tables:partsupp confirmed, columns:part.p_brand confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed
- **q13**: ✓ "number of orders" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "change year by year" → shape `time_trend`<br>✓ "orders … year by year between 1993 and 1997" → orders.o_orderdate = `1993..1997`
  - Label check: tables:customer confirmed, tables:orders confirmed, columns:customer.c_mktsegment confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:time_trend confirmed
- **q14**: ✓ "List" → shape `lookup`<br>✓ "quantity" → lineitem.l_quantity<br>✓ "ship mode" → lineitem.l_shipmode<br>✓ "shipping instruction" → lineitem.l_shipinstruct<br>✓ "line item" → lineitem<br>✓ "shipped on 1998-12-01" → lineitem.l_shipdate = `1998-12-01`
  - Label check: tables:lineitem confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipinstruct confirmed, columns:lineitem.l_shipmode confirmed, shapes:lookup confirmed
- **q15**: ✓ "share" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "CHINA" → nation.n_name = `CHINA`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
