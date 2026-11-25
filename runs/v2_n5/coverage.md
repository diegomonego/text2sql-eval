# Coverage report

- Generated: 2026-11-25T15:06:27+00:00 by `coverage_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 7cd82794b736dc1a0b94a142382d6c4310cd0cbb
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/v2_n5/questions.json, questions_sha256=f59d3d75ef786c7cb1ff69bf624637f25f15cc7efb3fd2fd2dc32dff75d56aef, n=5, issues_accepted=0

## Coverage by dimension

| dimension | covered | eligible | % |
|---|---|---|---|
| tables | 7 | 8 | 87.5 |
| columns | 14 | 61 | 22.95 |
| shapes | 7 | 8 | 87.5 |

- **Uncovered tables (1):** `partsupp`
- **Uncovered columns (47):** **customer**: `c_custkey`, `c_name`, `c_address`, `c_nationkey`, `c_phone`, `c_acctbal`, `c_mktsegment`, `c_comment`; **lineitem**: `l_orderkey`, `l_partkey`, `l_suppkey`, `l_linenumber`, `l_tax`, `l_returnflag`, `l_linestatus`, `l_shipinstruct`, `l_comment`; **nation**: `n_nationkey`, `n_regionkey`, `n_comment`; **orders**: `o_orderkey`, `o_custkey`, `o_orderstatus`, `o_totalprice`, `o_orderpriority`, `o_clerk`, `o_shippriority` (constant in this data), `o_comment`; **part**: `p_partkey`, `p_name`, `p_mfgr`, `p_brand`, `p_type`, `p_size`, `p_retailprice`, `p_comment`; **partsupp**: `ps_partkey`, `ps_suppkey`, `ps_availqty`, `ps_supplycost`, `ps_comment`; **region**: `r_regionkey`, `r_comment`; **supplier**: `s_suppkey`, `s_address`, `s_nationkey`, `s_comment`
- **Uncovered shapes (1):** `lookup`

## Budget

N = 5. There are 8 tables, 61 columns and 8 shapes. A few questions that each combine several tables and shapes can cover all tables and shapes; columns can't be covered that way. Credited questions here link 3.2 columns on average, so even with no repetition at most about 16 of 61 columns (26%) could be covered at this N; 14 were. Read column coverage relative to N. 0 question(s) earned no credit (a concept not in the database, or tables that don't connect) and 0 ambiguous phrase(s) earned nothing.

## Which questions cover each item

### Tables

| item | covered by |
|---|---|
| `customer` | q02, q03 |
| `lineitem` | q01, q03, q04 |
| `nation` | q01, q03 |
| `orders` | q02, q03 |
| `part` | q04 |
| `region` | q02, q05 |
| `supplier` | q01, q05 |

### Columns

| item | covered by |
|---|---|
| `lineitem.l_quantity` | q04 |
| `lineitem.l_extendedprice` | q03 |
| `lineitem.l_discount` | q03 |
| `lineitem.l_shipdate` | q04 |
| `lineitem.l_commitdate` | q01 |
| `lineitem.l_receiptdate` | q01 |
| `lineitem.l_shipmode` | q03 |
| `nation.n_name` | q01, q03 |
| `orders.o_orderdate` | q03 |
| `part.p_container` | q04 |
| `region.r_name` | q02, q05 |
| `supplier.s_name` | q05 |
| `supplier.s_phone` | q05 |
| `supplier.s_acctbal` | q05 |

### Shapes

| item | covered by |
|---|---|
| `aggregation` | q01, q02, q04 |
| `multi_join` | q01, q02, q03, q05 |
| `ranking` | q04 |
| `time_trend` | q01 |
| `ratio` | q03 |
| `vs_aggregate` | q05 |
| `anti_join` | q02 |

## Repetition

- Duplicate pairs (same tables, columns and shapes): none
- Questions covering nothing unique: none
- Questions earning no credit: none

## Summary score

**65.98** = (table % + column % + shape %) / 3 = (87.5 + 22.95 + 87.5) / 3 = 65.98

The three dimensions above, weighted equally. Tables and shapes fill up within a few questions, so at small N this number mostly tracks column coverage. Read the dimensions first.

## Per question

| id | question | credited | unique | not credited |
|---|---|---|---|---|
| q01 | How many line items from suppliers in the UNITED KINGDOM were received late in each year from 1993 to 1997? | tables: lineitem, nation, supplier; columns: lineitem.l_commitdate, lineitem.l_receiptdate, nation.n_name; shapes: aggregation, multi_join, time_trend | columns:lineitem.l_commitdate, columns:lineitem.l_receiptdate, shapes:time_trend | - |
| q02 | How many customers in the MIDDLE EAST region have never placed an order? | tables: customer, orders, region; columns: region.r_name; shapes: aggregation, anti_join, multi_join | shapes:anti_join | - |
| q03 | What percentage of revenue from orders placed by customers in INDONESIA last year came from items shipped by TRUCK? | tables: customer, lineitem, nation, orders; columns: lineitem.l_discount, lineitem.l_extendedprice, lineitem.l_shipmode, nation.n_name, orders.o_orderdate; shapes: multi_join, ratio | columns:lineitem.l_discount, columns:lineitem.l_extendedprice, columns:lineitem.l_shipmode, columns:orders.o_orderdate, shapes:ratio | - |
| q04 | Which 3 container types accounted for the largest quantity of units shipped this year? | tables: lineitem, part; columns: lineitem.l_quantity, lineitem.l_shipdate, part.p_container; shapes: aggregation, ranking | tables:part, columns:lineitem.l_quantity, columns:lineitem.l_shipdate, columns:part.p_container, shapes:ranking | - |
| q05 | List the names and phone numbers of suppliers in the ASIA region whose account balance is above that region's supplier average. | tables: region, supplier; columns: region.r_name, supplier.s_acctbal, supplier.s_name, supplier.s_phone; shapes: multi_join, vs_aggregate | columns:supplier.s_acctbal, columns:supplier.s_name, columns:supplier.s_phone, shapes:vs_aggregate | - |

## Links

- **q01**: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "UNITED KINGDOM" → nation.n_name = `UNITED KINGDOM`<br>✓ "received late" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "each year" → shape `time_trend`<br>✓ "received … from 1993 to 1997" → lineitem.l_receiptdate = `1993..1997`
  - Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:nation.n_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed
- **q02**: ✓ "How many" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST" → region.r_name = `MIDDLE EAST`<br>✓ "never" → shape `anti_join`<br>✓ "placed an order" → orders
  - Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed
- **q03**: ✓ "What percentage" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders" → orders<br>✓ "customers" → customer<br>✓ "INDONESIA" → nation.n_name = `INDONESIA`<br>✓ "placed … last year" → orders.o_orderdate = `1997`<br>✓ "items" → lineitem<br>✓ "shipped by TRUCK" → lineitem.l_shipmode = `TRUCK`
  - Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_shipmode confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
- **q04**: ✓ "Which 3 … largest" → shape `ranking`<br>✓ "container types" → part.p_container<br>✓ "accounted for" → shape `aggregation`<br>✓ "quantity of units" → lineitem.l_quantity<br>✓ "shipped this year" → lineitem.l_shipdate = `1998`
  - Label check: tables:lineitem confirmed, tables:part confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:part.p_container confirmed, shapes:ranking confirmed, shapes:aggregation not labeled
- **q05**: ✓ "names" → supplier.s_name<br>✓ "phone numbers" → supplier.s_phone<br>✓ "suppliers" → supplier<br>✓ "ASIA" → region.r_name = `ASIA`<br>✓ "account balance" → supplier.s_acctbal<br>✓ "above that region's supplier average" → shape `vs_aggregate`
  - Label check: tables:region confirmed, tables:supplier confirmed, columns:region.r_name confirmed, columns:supplier.s_acctbal confirmed, columns:supplier.s_name confirmed, columns:supplier.s_phone confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed
