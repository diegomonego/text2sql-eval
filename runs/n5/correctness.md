# Correctness report

- Generated: 2026-11-25T00:53:36+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: not a git repository
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/n5/questions.json, questions_sha256=0b0a76a088eda32a2edbd8965ae59b750a35092f9e1268632123993e8b407b61, n=5, issues_accepted=0

## Score

**1.0000** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (5 + 0.5 x 0) / 5 = 1.0000

| verdict | count |
|---|---|
| OFF_TOPIC | 0 |
| MISSING_DATA | 0 |
| AMBIGUOUS | 0 |
| ANSWERABLE | 5 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| q01 | What was the total profit on MEDIUM BRUSHED COPPER parts ordered by customers in JAPAN during 1995? | **ANSWERABLE** | Profit is defined in the glossary as l_extendedprice*(1-l_discount) - ps_supplycost*l_quantity; the part filter is p_type = 'MEDIUM BRUSHED COPPER', customers are filtered by nation.n_name = 'JAPAN', and 'ordered during 1995' maps to o_orderdate in 1995. |
| q02 | How many line items from suppliers in BRAZIL were delivered late in each year from 1993 to 1997? | **ANSWERABLE** | Late delivery is defined in the glossary as l_receiptdate > l_commitdate; suppliers are filtered by nation.n_name = 'BRAZIL', and 'delivered late in each year' groups by the delivery (receipt) year, l_receiptdate, over 1993-1997. |
| q03 | What percentage of line items from suppliers in the AMERICA region were returned? | **ANSWERABLE** | The glossary's coded-columns section defines l_returnflag = 'R' as returned; the share is R line items over all line items whose supplier's nation is in region.r_name = 'AMERICA'. |
| q04 | Which 3 brands have the highest average retail price among parts of size 50? | **ANSWERABLE** | Group parts with p_size = 50 by p_brand, average p_retailprice, and take the top 3; all columns are in the part table. |
| q05 | Which nations had total revenue from their customers' orders in 1996 above the average across all nations? | **ANSWERABLE** | Revenue is the glossary convention l_extendedprice*(1-l_discount); total it per customer nation (customer.c_nationkey -> nation) for orders with o_orderdate in 1996, then keep nations whose total exceeds the average of the per-nation totals. |

## Evidence

### q01: ANSWERABLE

> What was the total profit on MEDIUM BRUSHED COPPER parts ordered by customers in JAPAN during 1995?

Links: ✓ "total" → shape `aggregation`<br>✓ "profit" → lineitem.l_extendedprice, lineitem.l_discount, partsupp.ps_supplycost, lineitem.l_quantity<br>✓ "MEDIUM BRUSHED COPPER parts" → part.p_type = `MEDIUM BRUSHED COPPER`<br>✓ "customers" → customer<br>✓ "in JAPAN" → nation.n_name = `JAPAN`<br>✓ "ordered … during 1995" → orders.o_orderdate = `1995`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, tables:part confirmed, tables:partsupp confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:lineitem.l_quantity confirmed, columns:nation.n_name confirmed, columns:orders.o_orderdate confirmed, columns:part.p_type confirmed, columns:partsupp.ps_supplycost confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed

### q02: ANSWERABLE

> How many line items from suppliers in BRAZIL were delivered late in each year from 1993 to 1997?

Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "in BRAZIL" → nation.n_name = `BRAZIL`<br>✓ "delivered late" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "in each year" → shape `time_trend`<br>✓ "from 1993 to 1997" → lineitem.l_receiptdate = `1993..1997`

- Label check: tables:lineitem confirmed, tables:nation confirmed, tables:supplier confirmed, columns:lineitem.l_commitdate confirmed, columns:lineitem.l_receiptdate confirmed, columns:nation.n_name confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:time_trend confirmed

### q03: ANSWERABLE

> What percentage of line items from suppliers in the AMERICA region were returned?

Links: ✓ "percentage" → shape `ratio`<br>✓ "line items" → lineitem<br>✓ "suppliers" → supplier<br>✓ "AMERICA region" → region.r_name = `AMERICA`<br>✓ "returned" → lineitem.l_returnflag = `R`

- Label check: tables:lineitem confirmed, tables:region confirmed, tables:supplier confirmed, columns:lineitem.l_returnflag confirmed, columns:region.r_name confirmed, shapes:multi_join confirmed, shapes:ratio confirmed

### q04: ANSWERABLE

> Which 3 brands have the highest average retail price among parts of size 50?

Links: ✓ "highest" → shape `ranking`<br>✓ "brands" → part.p_brand<br>✓ "average" → shape `aggregation`<br>✓ "retail price" → part.p_retailprice<br>✓ "parts" → part<br>✓ "size 50" → part.p_size = `50`

- Label check: tables:part confirmed, columns:part.p_brand confirmed, columns:part.p_retailprice confirmed, columns:part.p_size confirmed, shapes:aggregation confirmed, shapes:ranking confirmed

### q05: ANSWERABLE

> Which nations had total revenue from their customers' orders in 1996 above the average across all nations?

Links: ✓ "nations" → nation<br>✓ "total" → shape `aggregation`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "customers" → customer<br>✓ "orders in 1996" → orders.o_orderdate = `1996`<br>✓ "above the average across all nations" → shape `vs_aggregate`

- Label check: tables:customer confirmed, tables:lineitem confirmed, tables:nation confirmed, tables:orders confirmed, columns:lineitem.l_discount confirmed, columns:lineitem.l_extendedprice confirmed, columns:orders.o_orderdate confirmed, shapes:aggregation confirmed, shapes:multi_join confirmed, shapes:vs_aggregate confirmed
