# Coverage report

- Generated: 2026-11-25T00:53:42+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n5/questions.json, questions_sha256=0b0a76a088eda32a2edbd8965ae59b750a35092f9e1268632123993e8b407b61, n=5, issues_accepted=0

## Score

**65.98** = (table % + column % + shape %) / 3 = (100.0 + 22.95 + 75.0) / 3 = 65.98

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 8 | 8 | 100.0 |
| columns | 14 | 61 | 22.95 |
| shapes | 6 | 8 | 75.0 |

## Budget

N = 5. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 3.8 columns on average, so even with no repetition at most about 19 of 61 columns (31%) could be covered at this N; 14 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: none
- Questions earning no credit: none

## Tables

| item | covered by |
|---|---|
| `customer` | q01, q05 |
| `lineitem` | q01, q02, q03, q05 |
| `nation` | q01, q02, q05 |
| `orders` | q01, q05 |
| `part` | q01, q04 |
| `partsupp` | q01 |
| `region` | q03 |
| `supplier` | q02, q03 |

## Columns

| item | covered by |
|---|---|
| `lineitem.l_quantity` | q01 |
| `lineitem.l_extendedprice` | q01, q05 |
| `lineitem.l_discount` | q01, q05 |
| `lineitem.l_returnflag` | q03 |
| `lineitem.l_commitdate` | q02 |
| `lineitem.l_receiptdate` | q02 |
| `nation.n_name` | q01, q02, q05 |
| `orders.o_orderdate` | q01, q05 |
| `part.p_brand` | q04 |
| `part.p_type` | q01 |
| `part.p_size` | q04 |
| `part.p_retailprice` | q04 |
| `partsupp.ps_supplycost` | q01 |
| `region.r_name` | q03 |
| `customer.c_custkey` | — not asked |
| `customer.c_name` | — not asked |
| `customer.c_address` | — not asked |
| `customer.c_nationkey` | — not asked |
| `customer.c_phone` | — not asked |
| `customer.c_acctbal` | — not asked |
| `customer.c_mktsegment` | — not asked |
| `customer.c_comment` | — not asked |
| `lineitem.l_orderkey` | — not asked |
| `lineitem.l_partkey` | — not asked |
| `lineitem.l_suppkey` | — not asked |
| `lineitem.l_linenumber` | — not asked |
| `lineitem.l_tax` | — not asked |
| `lineitem.l_linestatus` | — not asked |
| `lineitem.l_shipdate` | — not asked |
| `lineitem.l_shipinstruct` | — not asked |
| `lineitem.l_shipmode` | — not asked |
| `lineitem.l_comment` | — not asked |
| `nation.n_nationkey` | — not asked |
| `nation.n_regionkey` | — not asked |
| `nation.n_comment` | — not asked |
| `orders.o_orderkey` | — not asked |
| `orders.o_custkey` | — not asked |
| `orders.o_orderstatus` | — not asked |
| `orders.o_totalprice` | — not asked |
| `orders.o_orderpriority` | — not asked |
| `orders.o_clerk` | — not asked |
| `orders.o_shippriority` | — not asked (constant in this data) |
| `orders.o_comment` | — not asked |
| `part.p_partkey` | — not asked |
| `part.p_name` | — not asked |
| `part.p_mfgr` | — not asked |
| `part.p_container` | — not asked |
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
| `supplier.s_acctbal` | — not asked |
| `supplier.s_comment` | — not asked |

## Shapes

| item | covered by |
|---|---|
| `aggregation` | q01, q02, q04, q05 |
| `multi_join` | q01, q02, q03, q05 |
| `ranking` | q04 |
| `time_trend` | q02 |
| `ratio` | q03 |
| `vs_aggregate` | q05 |
| `lookup` | — not asked |
| `anti_join` | — not asked |

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | What was the total profit on MEDIUM BRUSHED COPPER parts ordered by customers in JAPAN during 1995? | tables: customer, lineitem, nation, orders, part, partsupp; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_quantity, nation.n_name, orders.o_orderdate, part.p_type, partsupp.ps_supplycost; shapes: aggregation, multi_join | tables:partsupp, columns:lineitem.l_quantity, columns:part.p_type, columns:partsupp.ps_supplycost | - |
| q02 | How many line items from suppliers in BRAZIL were delivered late in each year from 1993 to 1997? | tables: lineitem, nation, supplier; columns: lineitem.l_commitdate, lineitem.l_receiptdate, nation.n_name; shapes: aggregation, multi_join, time_trend | columns:lineitem.l_commitdate, columns:lineitem.l_receiptdate, shapes:time_trend | - |
| q03 | What percentage of line items from suppliers in the AMERICA region were returned? | tables: lineitem, region, supplier; columns: lineitem.l_returnflag, region.r_name; shapes: multi_join, ratio | tables:region, columns:lineitem.l_returnflag, columns:region.r_name, shapes:ratio | - |
| q04 | Which 3 brands have the highest average retail price among parts of size 50? | tables: part; columns: part.p_brand, part.p_retailprice, part.p_size; shapes: aggregation, ranking | columns:part.p_brand, columns:part.p_retailprice, columns:part.p_size, shapes:ranking | - |
| q05 | Which nations had total revenue from their customers' orders in 1996 above the average across all nations? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, lineitem.l_extendedprice, nation.n_name, orders.o_orderdate; shapes: aggregation, multi_join, vs_aggregate | shapes:vs_aggregate | - |

## Links

- **q01**: ✓ "total" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "MEDIUM BRUSHED COPPER parts" → part.p_type = `MEDIUM BRUSHED COPPER`<br>✓ "customers" → customer<br>✓ "JAPAN" → nation.n_name = `JAPAN`<br>✓ "ordered … during 1995" → orders.o_orderdate = `1995`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, tables:part confirmed, tables:partsupp confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:part.p_type confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed
- **q02**: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "BRAZIL" → nation.n_name = `BRAZIL`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "in each year" → shape `time_trend`<br>✓ "delivered … in each year from 1993 to 1997" → lineitem.l_receiptdate = `1993..1997`
  - Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:nation.n_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q03**: ✓ "What percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "AMERICA region" → region.r_name = `AMERICA`<br>✓ "returned" → lineitem.l_returnflag = `R`
  - Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_returnflag confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q04**: ✓ "3 brands have the highest" → shape `ranking`<br>✓ "brands" → part.p_brand<br>✓ "average" → shape `aggregation`<br>✓ "retail price" → part.p_retailprice<br>✓ "parts" → part<br>✓ "size 50" → part.p_size = `50`
  - Label check: tables:part confirmed, columns:part.p_brand confirmed, columns:part.p_retailprice confirmed, columns:part.p_size confirmed, shapes:aggregation confirmed, shapes:ranking confirmed
- **q05**: ✓ "nations" → nation.n_name<br>✓ "total" → shape `aggregation`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "customers'" → customer<br>✓ "orders in 1996" → orders.o_orderdate = `1996`<br>✓ "above the average across all nations" → shape `vs_aggregate`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:orders.o_orderdate confirmed, columns:nation.n_name not labeled, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed
