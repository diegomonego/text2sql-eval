# Coverage report

- Generated: 2026-11-25T00:48:27+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/smoke_n3/questions.json, questions_sha256=be5ecfaf266d216a6c36583daedc11814026c5c48e9199be8b1574569cb21732, n=3, issues_accepted=0

## Score

**54.37** = (table % + column % + shape %) / 3 = (87.5 + 13.11 + 62.5) / 3 = 54.37

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 7 | 8 | 87.5 |
| columns | 8 | 61 | 13.11 |
| shapes | 5 | 8 | 62.5 |

## Budget

N = 3. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 3.3 columns on average, so even with no repetition at most about 10 of 61 columns (16%) could be covered at this N; 8 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: none
- Questions earning no credit: none

## Tables

| item | covered by |
|---|---|
| `customer` | q02, q03 |
| `lineitem` | q01, q03 |
| `nation` | q03 |
| `orders` | q02, q03 |
| `partsupp` | q01 |
| `region` | q02 |
| `supplier` | q01 |
| `part` | — not asked |

## Columns

| item | covered by |
|---|---|
| `lineitem.l_quantity` | q01 |
| `lineitem.l_extendedprice` | q01, q03 |
| `lineitem.l_discount` | q01, q03 |
| `lineitem.l_shipdate` | q01 |
| `nation.n_name` | q03 |
| `orders.o_orderdate` | q03 |
| `partsupp.ps_supplycost` | q01 |
| `region.r_name` | q02 |
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
| `lineitem.l_returnflag` | — not asked |
| `lineitem.l_linestatus` | — not asked |
| `lineitem.l_commitdate` | — not asked |
| `lineitem.l_receiptdate` | — not asked |
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
| `part.p_brand` | — not asked |
| `part.p_type` | — not asked |
| `part.p_size` | — not asked |
| `part.p_container` | — not asked |
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
| `supplier.s_acctbal` | — not asked |
| `supplier.s_comment` | — not asked |

## Shapes

| item | covered by |
|---|---|
| `aggregation` | q01, q02 |
| `multi_join` | q01, q02, q03 |
| `ranking` | q01 |
| `ratio` | q03 |
| `anti_join` | q02 |
| `lookup` | — not asked |
| `time_trend` | — not asked |
| `vs_aggregate` | — not asked |

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | Which 5 suppliers earned the highest total profit on items shipped in 1997? | tables: lineitem, partsupp, supplier; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_quantity, lineitem.l_shipdate, partsupp.ps_supplycost; shapes: aggregation, multi_join, ranking | tables:partsupp, tables:supplier, columns:lineitem.l_quantity, columns:lineitem.l_shipdate, columns:partsupp.ps_supplycost, shapes:ranking | - |
| q02 | How many customers in the MIDDLE EAST region have never placed an order? | tables: customer, orders, region; columns: region.r_name; shapes: aggregation, anti_join, multi_join | tables:region, columns:region.r_name, shapes:anti_join | - |
| q03 | What share of revenue on orders placed in 1997 came from customers in the UNITED STATES? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, lineitem.l_extendedprice, nation.n_name, orders.o_orderdate; shapes: multi_join, ratio | tables:nation, columns:nation.n_name, columns:orders.o_orderdate, shapes:ratio | - |

## Links

- **q01**: ✓ "suppliers" → supplier<br>✓ "5 … highest" → shape `ranking`<br>✓ "total profit" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "items" → lineitem<br>✓ "shipped in 1997" → lineitem.l_shipdate = `1997`
  - Label check: tables:lineitem confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed
- **q02**: ✓ "How many" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "never" → shape `anti_join`<br>✓ "placed an order" → orders
  - Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q03**: ✓ "share" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "UNITED STATES" → nation.n_name = `UNITED STATES`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
