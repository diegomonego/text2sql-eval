# Coverage report

- Generated: 2026-11-25T00:53:40+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n10/questions.json, questions_sha256=58cb94ab7968684aa10e493194ec4cd4bd55d22614369b4440634e4f57b68b40, n=10, issues_accepted=0

## Score

**77.05** = (table % + column % + shape %) / 3 = (100.0 + 31.15 + 100.0) / 3 = 77.05

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 8 | 8 | 100.0 |
| columns | 19 | 61 | 31.15 |
| shapes | 8 | 8 | 100.0 |

## Budget

N = 10. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 3.4 columns on average, so even with no repetition at most about 34 of 61 columns (56%) could be covered at this N; 19 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: q05, q07
- Questions earning no credit: none

## Tables

| item | covered by |
|---|---|
| `customer` | q02, q05, q07, q08 |
| `lineitem` | q01, q03, q04, q05, q08, q09 |
| `nation` | q01, q07, q08, q10 |
| `orders` | q02, q05, q06, q07, q08 |
| `part` | q03, q09 |
| `partsupp` | q01 |
| `region` | q02, q04, q05 |
| `supplier` | q01, q04, q10 |

## Columns

| item | covered by |
|---|---|
| `customer.c_mktsegment` | q02 |
| `lineitem.l_quantity` | q01 |
| `lineitem.l_extendedprice` | q01, q03, q05, q09 |
| `lineitem.l_discount` | q01, q03, q05, q09 |
| `lineitem.l_shipdate` | q01, q03, q09 |
| `lineitem.l_commitdate` | q04 |
| `lineitem.l_receiptdate` | q04 |
| `lineitem.l_shipinstruct` | q08 |
| `nation.n_name` | q01, q07, q08 |
| `orders.o_orderstatus` | q06 |
| `orders.o_totalprice` | q06, q07 |
| `orders.o_orderdate` | q05, q06, q07, q08 |
| `orders.o_orderpriority` | q06 |
| `orders.o_clerk` | q06 |
| `part.p_mfgr` | q03 |
| `part.p_container` | q09 |
| `partsupp.ps_supplycost` | q01 |
| `region.r_name` | q02, q04 |
| `supplier.s_acctbal` | q10 |
| `customer.c_custkey` | — not asked |
| `customer.c_name` | — not asked |
| `customer.c_address` | — not asked |
| `customer.c_nationkey` | — not asked |
| `customer.c_phone` | — not asked |
| `customer.c_acctbal` | — not asked |
| `customer.c_comment` | — not asked |
| `lineitem.l_orderkey` | — not asked |
| `lineitem.l_partkey` | — not asked |
| `lineitem.l_suppkey` | — not asked |
| `lineitem.l_linenumber` | — not asked |
| `lineitem.l_tax` | — not asked |
| `lineitem.l_returnflag` | — not asked |
| `lineitem.l_linestatus` | — not asked |
| `lineitem.l_shipmode` | — not asked |
| `lineitem.l_comment` | — not asked |
| `nation.n_nationkey` | — not asked |
| `nation.n_regionkey` | — not asked |
| `nation.n_comment` | — not asked |
| `orders.o_orderkey` | — not asked |
| `orders.o_custkey` | — not asked |
| `orders.o_shippriority` | — not asked (constant in this data) |
| `orders.o_comment` | — not asked |
| `part.p_partkey` | — not asked |
| `part.p_name` | — not asked |
| `part.p_brand` | — not asked |
| `part.p_type` | — not asked |
| `part.p_size` | — not asked |
| `part.p_retailprice` | — not asked |
| `part.p_comment` | — not asked |
| `partsupp.ps_partkey` | — not asked |
| `partsupp.ps_suppkey` | — not asked |
| `partsupp.ps_availqty` | — not asked |
| `partsupp.ps_comment` | — not asked |
| `region.r_regionkey` | — not asked |
| `region.r_comment` | — not asked |
| `supplier.s_suppkey` | — not asked |
| `supplier.s_name` | — not asked |
| `supplier.s_address` | — not asked |
| `supplier.s_nationkey` | — not asked |
| `supplier.s_phone` | — not asked |
| `supplier.s_comment` | — not asked |

## Shapes

| item | covered by |
|---|---|
| `lookup` | q06 |
| `aggregation` | q01, q02, q03, q05, q07, q09, q10 |
| `multi_join` | q01, q02, q04, q05, q07, q08 |
| `ranking` | q01, q09 |
| `time_trend` | q03, q07 |
| `ratio` | q04, q08 |
| `vs_aggregate` | q05, q10 |
| `anti_join` | q02 |

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | Which 5 suppliers in RUSSIA earned the highest total profit on items shipped in 1996? | tables: lineitem, nation, partsupp, supplier; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_quantity, lineitem.l_shipdate, nation.n_name, partsupp.ps_supplycost; shapes: aggregation, multi_join, ranking | tables:partsupp, columns:lineitem.l_quantity, columns:partsupp.ps_supplycost | - |
| q02 | How many MACHINERY customers in the ASIA region have never placed an order? | tables: customer, orders, region; columns: customer.c_mktsegment, region.r_name; shapes: aggregation, anti_join, multi_join | columns:customer.c_mktsegment, shapes:anti_join | - |
| q03 | How did total revenue from Manufacturer#4 parts change year by year for items shipped between 1993 and 1997? | tables: lineitem, part; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_shipdate, part.p_mfgr; shapes: aggregation, time_trend | columns:part.p_mfgr | - |
| q04 | What proportion of line items received in 1995 from suppliers in the MIDDLE EAST region were delivered late? | tables: lineitem, region, supplier; columns: lineitem.l_commitdate, lineitem.l_receiptdate, region.r_name; shapes: multi_join, ratio | columns:lineitem.l_commitdate, columns:lineitem.l_receiptdate | - |
| q05 | Which regions generated more revenue from their customers' orders placed in 1997 than the average region? | tables: customer, lineitem, orders, region; columns: lineitem.l_discount, lineitem.l_extendedprice, orders.o_orderdate; shapes: aggregation, multi_join, vs_aggregate | nothing | - |
| q06 | List the clerk, order value and status of each 5-LOW priority order placed on 1 July 1998. | tables: orders; columns: orders.o_clerk, orders.o_orderdate, orders.o_orderpriority, orders.o_orderstatus, orders.o_totalprice; shapes: lookup | columns:orders.o_clerk, columns:orders.o_orderpriority, columns:orders.o_orderstatus, shapes:lookup | - |
| q07 | How did the total order value from customers in BRAZIL change quarter by quarter in 1997? | tables: customer, nation, orders; columns: nation.n_name, orders.o_orderdate, orders.o_totalprice; shapes: aggregation, multi_join, time_trend | nothing | - |
| q08 | What percentage of the line items ordered by customers in KENYA during 1997 carried the shipping instruction COLLECT COD? | tables: customer, lineitem, nation, orders; columns: lineitem.l_shipinstruct, nation.n_name, orders.o_orderdate; shapes: multi_join, ratio | columns:lineitem.l_shipinstruct | - |
| q09 | Which 5 parts packed in LG CASE containers brought in the highest total revenue from items shipped in 1996? | tables: lineitem, part; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_shipdate, part.p_container; shapes: aggregation, ranking | columns:part.p_container | - |
| q10 | Which nations have a mean supplier account balance higher than the average across all suppliers? | tables: nation, supplier; columns: supplier.s_acctbal; shapes: aggregation, vs_aggregate | columns:supplier.s_acctbal | - |

## Links

- **q01**: ✓ "suppliers" → supplier<br>✓ "RUSSIA" → nation.n_name = `RUSSIA`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "shipped in 1996" → lineitem.l_shipdate = `1996`<br>✓ "total" → shape `aggregation`<br>✓ "5 … highest" → shape `ranking`
  - Label check: tables:lineitem confirmed, tables:nation confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:nation.n_name confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed
- **q02**: ✓ "customers" → customer<br>✓ "MACHINERY" → customer.c_mktsegment = `MACHINERY`<br>✓ "ASIA region" → region.r_name = `ASIA`<br>✓ "order" → orders<br>✓ "How many" → shape `aggregation`<br>✓ "never placed an order" → shape `anti_join`
  - Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:customer.c_mktsegment confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q03**: ✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "Manufacturer#4" → part.p_mfgr = `Manufacturer#4`<br>✓ "parts" → part<br>✓ "shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`<br>✓ "total" → shape `aggregation`<br>✓ "change year by year" → shape `time_trend`
  - Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_mfgr confirmed, shapes:aggregation confirmed, shapes:time_trend confirmed
- **q04**: ✓ "line items" → lineitem<br>✓ "received in 1995" → lineitem.l_receiptdate = `1995`<br>✓ "suppliers" → supplier<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "proportion" → shape `ratio`
  - Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q05**: ✓ "regions" → region<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "customers'" → customer<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "generated more revenue" → shape `aggregation`<br>✓ "more … than the average region" → shape `vs_aggregate`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:orders confirmed, tables:region confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed, shapes:aggregation not labeled
- **q06**: ✓ "clerk" → orders.o_clerk<br>✓ "order value" → orders.o_totalprice<br>✓ "status" → orders.o_orderstatus<br>✓ "5-LOW priority" → orders.o_orderpriority = `5-LOW`<br>✓ "placed on 1 July 1998" → orders.o_orderdate = `1998-07-01`<br>✓ "List" → shape `lookup`
  - Label check: tables:orders confirmed, columns:orders.o_clerk confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_orderpriority confirmed, columns:orders.o_orderstatus confirmed, columns:orders.o_totalprice confirmed, shapes:lookup confirmed
- **q07**: ✓ "order value" → orders.o_totalprice<br>✓ "customers" → customer<br>✓ "BRAZIL" → nation.n_name = `BRAZIL`<br>✓ "in 1997" → orders.o_orderdate = `1997`<br>✓ "total" → shape `aggregation`<br>✓ "change quarter by quarter" → shape `time_trend`
  - Label check: tables:customer confirmed, tables:nation confirmed, tables:orders confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:orders.o_totalprice confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q08**: ✓ "line items" → lineitem<br>✓ "customers" → customer<br>✓ "KENYA" → nation.n_name = `KENYA`<br>✓ "ordered … during 1997" → orders.o_orderdate = `1997`<br>✓ "shipping instruction COLLECT COD" → lineitem.l_shipinstruct = `COLLECT COD`<br>✓ "percentage" → shape `ratio`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_shipinstruct confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q09**: ✓ "parts" → part<br>✓ "LG CASE containers" → part.p_container = `LG CASE`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "shipped in 1996" → lineitem.l_shipdate = `1996`<br>✓ "total" → shape `aggregation`<br>✓ "5 … highest" → shape `ranking`
  - Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_container confirmed, shapes:aggregation confirmed, shapes:ranking confirmed
- **q10**: ✓ "nations" → nation<br>✓ "supplier account balance" → supplier.s_acctbal<br>✓ "suppliers" → supplier<br>✓ "mean" → shape `aggregation`<br>✓ "higher than the average across all suppliers" → shape `vs_aggregate`
  - Label check: tables:nation confirmed, tables:supplier confirmed, columns:supplier.s_acctbal confirmed, shapes:aggregation confirmed, shapes:vs_aggregate confirmed
