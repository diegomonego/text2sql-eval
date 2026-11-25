# Coverage report

- Generated: 2026-11-25T00:54:04+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n15/questions.json, questions_sha256=7dd977525fff7199a91884b99e7994c58661b8ed134cce569d73f8a60d4787ec, n=15, issues_accepted=0

## Score

**83.06** = (table % + column % + shape %) / 3 = (100.0 + 49.18 + 100.0) / 3 = 83.06

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 8 | 8 | 100.0 |
| columns | 30 | 61 | 49.18 |
| shapes | 8 | 8 | 100.0 |

## Budget

N = 15. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 3.2 columns on average, so even with no repetition at most about 48 of 61 columns (79%) could be covered at this N; 30 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: q03, q04, q08, q10, q12
- Questions earning no credit: none

## Tables

| item | covered by |
|---|---|
| `customer` | q02, q04, q08, q09 |
| `lineitem` | q01, q05, q08, q11, q12, q13 |
| `nation` | q01, q02, q04, q09, q11 |
| `orders` | q02, q04, q14 |
| `part` | q03, q06, q07 |
| `partsupp` | q01, q07, q10 |
| `region` | q03, q05, q08 |
| `supplier` | q01, q03, q05, q07, q10, q11, q15 |

## Columns

| item | covered by |
|---|---|
| `customer.c_name` | q09 |
| `customer.c_phone` | q09 |
| `customer.c_acctbal` | q09 |
| `customer.c_mktsegment` | q09 |
| `lineitem.l_quantity` | q01 |
| `lineitem.l_extendedprice` | q01, q12 |
| `lineitem.l_discount` | q01 |
| `lineitem.l_returnflag` | q05 |
| `lineitem.l_shipdate` | q01, q08, q11, q12, q13 |
| `lineitem.l_commitdate` | q13 |
| `lineitem.l_receiptdate` | q05, q13 |
| `lineitem.l_shipinstruct` | q11 |
| `lineitem.l_shipmode` | q08, q13 |
| `nation.n_name` | q01, q02, q09, q11 |
| `orders.o_totalprice` | q04, q14 |
| `orders.o_orderdate` | q02, q04, q14 |
| `orders.o_orderpriority` | q02 |
| `orders.o_clerk` | q14 |
| `part.p_name` | q06 |
| `part.p_brand` | q03, q06 |
| `part.p_type` | q07 |
| `part.p_size` | q06 |
| `part.p_container` | q06 |
| `part.p_retailprice` | q06 |
| `partsupp.ps_availqty` | q07, q10 |
| `partsupp.ps_supplycost` | q01 |
| `region.r_name` | q03, q05, q08 |
| `supplier.s_name` | q15 |
| `supplier.s_phone` | q15 |
| `supplier.s_acctbal` | q10, q15 |
| `customer.c_custkey` | — not asked |
| `customer.c_address` | — not asked |
| `customer.c_nationkey` | — not asked |
| `customer.c_comment` | — not asked |
| `lineitem.l_orderkey` | — not asked |
| `lineitem.l_partkey` | — not asked |
| `lineitem.l_suppkey` | — not asked |
| `lineitem.l_linenumber` | — not asked |
| `lineitem.l_tax` | — not asked |
| `lineitem.l_linestatus` | — not asked |
| `lineitem.l_comment` | — not asked |
| `nation.n_nationkey` | — not asked |
| `nation.n_regionkey` | — not asked |
| `nation.n_comment` | — not asked |
| `orders.o_orderkey` | — not asked |
| `orders.o_custkey` | — not asked |
| `orders.o_orderstatus` | — not asked |
| `orders.o_shippriority` | — not asked (constant in this data) |
| `orders.o_comment` | — not asked |
| `part.p_partkey` | — not asked |
| `part.p_mfgr` | — not asked |
| `part.p_comment` | — not asked |
| `partsupp.ps_partkey` | — not asked |
| `partsupp.ps_suppkey` | — not asked |
| `partsupp.ps_comment` | — not asked |
| `region.r_regionkey` | — not asked |
| `region.r_comment` | — not asked |
| `supplier.s_suppkey` | — not asked |
| `supplier.s_address` | — not asked |
| `supplier.s_nationkey` | — not asked |
| `supplier.s_comment` | — not asked |

## Shapes

| item | covered by |
|---|---|
| `lookup` | q06, q09, q15 |
| `aggregation` | q01, q02, q04, q07, q08, q10, q12, q14 |
| `multi_join` | q01, q02, q03, q04, q05, q07, q08, q11 |
| `ranking` | q02, q07, q14 |
| `time_trend` | q01, q08 |
| `ratio` | q05, q10, q13 |
| `vs_aggregate` | q04, q12 |
| `anti_join` | q03, q11 |

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | How did the total profit on items supplied by suppliers in FRANCE change year by year for shipments between 1993 and 1997? | tables: lineitem, nation, partsupp, supplier; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_quantity, lineitem.l_shipdate, nation.n_name, partsupp.ps_supplycost; shapes: aggregation, multi_join, time_trend | columns:lineitem.l_discount, columns:lineitem.l_quantity, columns:partsupp.ps_supplycost | - |
| q02 | Which 5 customers in INDIA placed the largest number of 1-URGENT orders in 1997? | tables: customer, nation, orders; columns: nation.n_name, orders.o_orderdate, orders.o_orderpriority; shapes: aggregation, multi_join, ranking | columns:orders.o_orderpriority | - |
| q03 | Which Brand#23 parts have no supplier located in the ASIA region? | tables: part, region, supplier; columns: part.p_brand, region.r_name; shapes: anti_join, multi_join | nothing | - |
| q04 | Which nations had a total order value from their customers in 1995 above the average across all nations? | tables: customer, nation, orders; columns: orders.o_orderdate, orders.o_totalprice; shapes: aggregation, multi_join, vs_aggregate | nothing | - |
| q05 | Of the line items received in 1994 from suppliers in the AFRICA region, what fraction were returned? | tables: lineitem, region, supplier; columns: lineitem.l_receiptdate, lineitem.l_returnflag, region.r_name; shapes: multi_join, ratio | columns:lineitem.l_returnflag | - |
| q06 | List the name, brand and retail price of every part of size 49 packed in an LG DRUM container. | tables: part; columns: part.p_brand, part.p_container, part.p_name, part.p_retailprice, part.p_size; shapes: lookup | columns:part.p_container, columns:part.p_name, columns:part.p_retailprice, columns:part.p_size | - |
| q07 | Which 5 suppliers hold the largest total available quantity of STEEL parts? | tables: part, partsupp, supplier; columns: part.p_type, partsupp.ps_availqty; shapes: aggregation, multi_join, ranking | columns:part.p_type | - |
| q08 | How did the number of line items shipped by FOB to customers in the MIDDLE EAST region change quarter by quarter in 1996? | tables: customer, lineitem, region; columns: lineitem.l_shipdate, lineitem.l_shipmode, region.r_name; shapes: aggregation, multi_join, time_trend | nothing | - |
| q09 | List the name and phone number of customers in the AUTOMOBILE segment in CANADA with a negative account balance. | tables: customer, nation; columns: customer.c_acctbal, customer.c_mktsegment, customer.c_name, customer.c_phone, nation.n_name; shapes: lookup | columns:customer.c_acctbal, columns:customer.c_mktsegment, columns:customer.c_name, columns:customer.c_phone | - |
| q10 | What share of our suppliers' combined available quantity is held by suppliers with a negative account balance? | tables: partsupp, supplier; columns: partsupp.ps_availqty, supplier.s_acctbal; shapes: aggregation, ratio | nothing | - |
| q11 | Which suppliers in PERU had no line items with the shipping instruction COLLECT COD shipped last month? | tables: lineitem, nation, supplier; columns: lineitem.l_shipdate, lineitem.l_shipinstruct, nation.n_name; shapes: anti_join, multi_join | columns:lineitem.l_shipinstruct | - |
| q12 | How many line items shipped in 1995 had a gross value above that year's average? | tables: lineitem; columns: lineitem.l_extendedprice, lineitem.l_shipdate; shapes: aggregation, vs_aggregate | nothing | - |
| q13 | What percentage of line items shipped by MAIL in 1996 were delivered late? | tables: lineitem; columns: lineitem.l_commitdate, lineitem.l_receiptdate, lineitem.l_shipdate, lineitem.l_shipmode; shapes: ratio | columns:lineitem.l_commitdate | - |
| q14 | Which 10 clerks handled the highest total order value in 1996? | tables: orders; columns: orders.o_clerk, orders.o_orderdate, orders.o_totalprice; shapes: aggregation, ranking | columns:orders.o_clerk | - |
| q15 | What is the phone number and account balance of Supplier#000000427? | tables: supplier; columns: supplier.s_acctbal, supplier.s_name, supplier.s_phone; shapes: lookup | columns:supplier.s_name, columns:supplier.s_phone | - |

## Links

- **q01**: ✓ "total profit" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "FRANCE" → nation.n_name = `FRANCE`<br>✓ "change year by year" → shape `time_trend`<br>✓ "shipments between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`
  - Label check: tables:lineitem confirmed, tables:nation confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:nation.n_name confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q02**: ✓ "5 customers … largest" → shape `ranking`<br>✓ "customers" → customer<br>✓ "INDIA" → nation.n_name = `INDIA`<br>✓ "number of" → shape `aggregation`<br>✓ "1-URGENT orders" → orders.o_orderpriority = `1-URGENT`<br>✓ "placed … in 1997" → orders.o_orderdate = `1997`
  - Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed
- **q03**: ✓ "Brand#23" → part.p_brand = `Brand#23`<br>✓ "parts" → part<br>✓ "have no supplier" → shape `anti_join`<br>✓ "supplier" → supplier<br>✓ "ASIA region" → region.r_name = `ASIA`
  - Label check: tables:part confirmed, tables:region confirmed, tables:supplier confirmed, columns:part.p_brand confirmed, columns:region.r_name confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q04**: ✓ "nations" → nation<br>✓ "total order value" → shape `aggregation`<br>✓ "order value" → orders.o_totalprice<br>✓ "customers" → customer<br>✓ "order value … in 1995" → orders.o_orderdate = `1995`<br>✓ "above the average across all nations" → shape `vs_aggregate`
  - Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed
- **q05**: ✓ "line items" → lineitem<br>✓ "received in 1994" → lineitem.l_receiptdate = `1994`<br>✓ "suppliers" → supplier<br>✓ "AFRICA region" → region.r_name = `AFRICA`<br>✓ "what fraction" → shape `ratio`<br>✓ "returned" → lineitem.l_returnflag = `R`
  - Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_returnflag confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q06**: ✓ "List" → shape `lookup`<br>✓ "name" → part.p_name<br>✓ "brand" → part.p_brand<br>✓ "retail price" → part.p_retailprice<br>✓ "part" → part<br>✓ "size 49" → part.p_size = `49`<br>✓ "LG DRUM container" → part.p_container = `LG DRUM`
  - Label check: tables:part confirmed, columns:part.p_brand confirmed, columns:part.p_container confirmed, columns:part.p_name confirmed, columns:part.p_retailprice confirmed, columns:part.p_size confirmed, shapes:lookup confirmed
- **q07**: ✓ "5 suppliers … largest" → shape `ranking`<br>✓ "suppliers" → supplier<br>✓ "total available quantity" → shape `aggregation`<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "STEEL parts" → part.p_type = `STEEL` (contains)
  - Label check: tables:part confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:part.p_type confirmed, columns:partsupp.ps_availqty confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed
- **q08**: ✓ "number of" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "shipped by FOB" → lineitem.l_shipmode = `FOB`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "change quarter by quarter" → shape `time_trend`<br>✓ "shipped … in 1996" → lineitem.l_shipdate = `1996`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:region confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q09**: ✓ "List" → shape `lookup`<br>✓ "name" → customer.c_name<br>✓ "phone number" → customer.c_phone<br>✓ "customers" → customer<br>✓ "AUTOMOBILE segment" → customer.c_mktsegment = `AUTOMOBILE`<br>✓ "CANADA" → nation.n_name = `CANADA`<br>✓ "negative account balance" → customer.c_acctbal
  - Label check: tables:customer confirmed, tables:nation confirmed, columns:customer.c_acctbal confirmed, columns:customer.c_mktsegment confirmed, columns:customer.c_name confirmed, columns:customer.c_phone confirmed, columns:nation.n_name confirmed, shapes:lookup confirmed
- **q10**: ✓ "What share" → shape `ratio`<br>✓ "suppliers'" → supplier<br>✓ "combined available quantity" → shape `aggregation`<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "negative account balance" → supplier.s_acctbal
  - Label check: tables:partsupp confirmed, tables:supplier confirmed, columns:partsupp.ps_availqty confirmed, columns:supplier.s_acctbal confirmed, shapes:ratio confirmed, shapes:aggregation not labeled
- **q11**: ✓ "suppliers" → supplier<br>✓ "PERU" → nation.n_name = `PERU`<br>✓ "had no line items" → shape `anti_join`<br>✓ "line items" → lineitem<br>✓ "shipping instruction COLLECT COD" → lineitem.l_shipinstruct = `COLLECT COD`<br>✓ "shipped last month" → lineitem.l_shipdate = `1998-07`
  - Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipinstruct confirmed, columns:nation.n_name confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q12**: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "shipped in 1995" → lineitem.l_shipdate = `1995`<br>✓ "gross value" → lineitem.l_extendedprice<br>✓ "above that year's average" → shape `vs_aggregate`
  - Label check: tables:lineitem confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed
- **q13**: ✓ "What percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "shipped by MAIL" → lineitem.l_shipmode = `MAIL`<br>✓ "shipped … in 1996" → lineitem.l_shipdate = `1996`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate
  - Label check: tables:lineitem confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:lineitem.l_shipdate confirmed, columns:lineitem.l_shipmode confirmed, shapes:ratio confirmed
- **q14**: ✓ "10 clerks … highest" → shape `ranking`<br>✓ "clerks" → orders.o_clerk<br>✓ "total order value" → shape `aggregation`<br>✓ "order value" → orders.o_totalprice<br>✓ "order value in 1996" → orders.o_orderdate = `1996`
  - Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:ranking confirmed
- **q15**: ✓ "What is" → shape `lookup`<br>✓ "phone number" → supplier.s_phone<br>✓ "account balance" → supplier.s_acctbal<br>✓ "Supplier#000000427" → supplier.s_name = `Supplier#000000427`
  - Label check: tables:supplier confirmed, columns:supplier.s_acctbal confirmed, columns:supplier.s_name confirmed, columns:supplier.s_phone confirmed, shapes:lookup confirmed
