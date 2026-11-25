# Correctness report

- Generated: 2026-11-25T00:47:56+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/smoke_n3/questions.json, questions_sha256=be5ecfaf266d216a6c36583daedc11814026c5c48e9199be8b1574569cb21732, n=3, issues_accepted=0

## Score

**1.0000** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (3 + 0.5 x 0) / 3 = 1.0000

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 0 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 3 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | Which 5 suppliers earned the highest total profit on items shipped in 1997? | **ANSWERABLE** | Profit is defined in the glossary (Money: Profit) as l_extendedprice × (1 − l_discount) − ps_supplycost × l_quantity, with partsupp joined on the line's part and supplier; 'shipped in 1997' filters lineitem.l_shipdate, and suppliers are ranked by summed profit. |
| q02 | How many customers in the MIDDLE EAST region have never placed an order? | **ANSWERABLE** | Count customers whose nation belongs to region.r_name = 'MIDDLE EAST' (customer → nation → region) and who have no row in orders (anti-join on orders.o_custkey); spec clause 1.4 notes one-third of customers have no orders. |
| q03 | What share of revenue on orders placed in 1997 came from customers in the UNITED STATES? | **ANSWERABLE** | Revenue is defined in the glossary as l_extendedprice × (1 − l_discount); the share is revenue of 1997 orders (orders.o_orderdate) from customers whose nation.n_name = 'UNITED STATES' divided by revenue of all 1997 orders. |

## Evidence

### q01: ANSWERABLE

> Which 5 suppliers earned the highest total profit on items shipped in 1997?

Links: ✓ "suppliers" → supplier<br>✓ "5" → shape `ranking`<br>✓ "highest" → shape `ranking`<br>✓ "total" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "items" → lineitem<br>✓ "shipped in 1997" → lineitem.l_shipdate = `1997`

- Label check: tables:lineitem confirmed, tables:partsupp confirmed, tables:supplier confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:lineitem.l_shipdate confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:ranking confirmed

### q02: ANSWERABLE

> How many customers in the MIDDLE EAST region have never placed an order?

Links: ✓ "How many" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "MIDDLE EAST region" → region.r_name = `MIDDLE EAST`<br>✓ "never" → shape `anti_join`<br>✓ "placed an order" → orders

- Label check: tables:customer confirmed, tables:orders confirmed, tables:region confirmed, columns:region.r_name confirmed, shapes:aggregation confirmed, shapes:anti_join confirmed, shapes:multi_join confirmed

### q03: ANSWERABLE

> What share of revenue on orders placed in 1997 came from customers in the UNITED STATES?

Links: ✓ "share" → shape `ratio`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "orders placed in 1997" → orders.o_orderdate = `1997`<br>✓ "customers" → customer<br>✓ "UNITED STATES" → nation.n_name = `UNITED STATES`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, shapes:multi_join confirmed, shapes:ratio confirmed
