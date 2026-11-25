# Correctness report

- Generated: 2026-11-25T15:23:29+00:00 by `correctness_judge`, model `claude-opus-5-5`, 2.1.331 (Claude Code)
- Git: 7cd82794b736dc1a0b94a142382d6c4310cd0cbb
- Database: `duckdb:///data/tpch_sf01.duckdb` (duckdb 2.0.1, 8 tables, 61 columns, sha256 `9a6859c7dad2`)
- Docs: semantic_docs/tpch/glossary.md, semantic_docs/tpch/spec/clause1_database_design.md, semantic_docs/tpch/spec/clause4_data_generation.md
- Time anchor: auto (1998-08-02)
- Input: questions_file=runs/labeled_20/questions.json, questions_sha256=816641734de0640ee7ea5860edf9ca8feded6c33b8995bb0e609fc949949f5eb, n=20, issues_accepted=0

## Score

**0.3750** = (ANSWERABLE + 0.5 x AMBIGUOUS) / N = (5 + 0.5 x 5) / 20 = 0.3750

| verdict | count |
|---|---|
| OFF_TOPIC | 1 |
| MISSING_DATA | 9 |
| AMBIGUOUS | 5 |
| ANSWERABLE | 5 |

Verdicts whose evidence failed a code check: 0.

## Verdicts

| id | question | verdict | rationale |
|---|---|---|---|
| l01 | What is the average price of a part? | **AMBIGUOUS** | "Price of a part" fits the list price part.p_retailprice, the supply cost partsupp.ps_supplycost (what the wholesaler pays per unit), and the realized per-unit selling price from lineitem (extended price after discount over quantity). The docs don't say which one 'price' means, and the averages differ a lot (about 1,400 vs about 500). |
| l02 | What is the average customer satisfaction rating per market segment? | **MISSING_DATA** | Market segment is customer.c_mktsegment, but no table stores satisfaction ratings or feedback, and none can be derived (comments are generated filler text, per the glossary's 'Free text'). |
| l03 | Which clerks exceeded their quarterly sales targets in 1996? | **MISSING_DATA** | Clerks are orders.o_clerk and 1996 sales can be computed, but the schema has no sales targets or quotas for clerks, so 'exceeded their targets' can't be evaluated. |
| l04 | What was the average number of orders per customer in 1995? | **AMBIGUOUS** | Orders in 1995 are counted on orders.o_orderdate, but the denominator 'per customer' could be only the customers who ordered in 1995 or all 15,000 customers in customer (a third of them never order, per the spec). The two averages differ materially. |
| l05 | Which 10 parts of size 50 have the lowest total available quantity across all suppliers? | **ANSWERABLE** | Filter part.p_size = 50, sum partsupp.ps_availqty over each part's supplier rows, and return the 10 smallest totals. 'Available quantity' is ps_availqty per the glossary (Parts). |
| l06 | What is the population of GERMANY? | **MISSING_DATA** | GERMANY is a nation.n_name value, but the nation table holds only key, name, region and filler comment; no population or demographic data exists. |
| l07 | In which countries is the average account balance of customers higher than the overall average for all customers? | **ANSWERABLE** | Average customer.c_acctbal per customer nation (nation.n_name via c_nationkey), keeping nations whose average is above AVG(c_acctbal) over all customers. Only customers are involved, so 'countries' can only be the customers' nation. |
| l08 | Which customers placed large orders in 1997? | **AMBIGUOUS** | The docs don't define 'large'. It could mean high order value (orders.o_totalprice) or high quantity (lineitem.l_quantity), and any threshold is arbitrary, so different readings return different customers. |
| l09 | What is the average weight of parts shipped by TRUCK? | **MISSING_DATA** | Shipped by TRUCK is lineitem.l_shipmode = 'TRUCK', but parts have no weight attribute. p_size is a size code, not a weight. |
| l10 | For line items shipped between 1993 and 1997 to customers in ASIA, how did the average time from shipment to receipt change each year? | **ANSWERABLE** | Shipping time is l_receiptdate - l_shipdate (glossary: Shipping time). Filter l_shipdate in 1993-1997 and customers whose nation is in region ASIA (orders -> customer -> nation -> region), then average per ship year. Grouping by ship year follows from the ship-date filter; I rejected order year as a weaker reading. |
| l11 | How did the number of late deliveries from suppliers in INDIA change year by year for items received between 1993 and 1997? | **ANSWERABLE** | Late delivery is l_receiptdate > l_commitdate (glossary: Late delivery). Restrict to suppliers whose nation.n_name = 'INDIA' and l_receiptdate in 1993-1997, then count per receipt year. |
| l12 | Who won the FIFA World Cup in 1998? | **OFF_TOPIC** | Football results have nothing to do with the wholesale parts business the database describes. |
| l13 | How did the available quantity of Brand#23 parts change month by month during 1997? | **MISSING_DATA** | Brand#23 is part.p_brand, but partsupp.ps_availqty is one undated value per part and supplier. No inventory history exists, so there is no month-by-month change to report. |
| l14 | Which cities had the most late deliveries in 1996? | **MISSING_DATA** | Late deliveries can be computed (glossary: l_receiptdate > l_commitdate), but no city is stored. c_address and s_address are random strings (spec 4.2.3), and the finest geography is nation. |
| l15 | How many line items did we have in March 1996? | **AMBIGUOUS** | Line items have no single date: 'in March 1996' could filter on the order date (orders.o_orderdate), the ship date (l_shipdate) or the receipt date (l_receiptdate), which give different counts. The docs don't pick one. |
| l16 | What was the total freight cost paid to carriers for AIR shipments in 1996? | **MISSING_DATA** | AIR shipments are lineitem.l_shipmode = 'AIR', but no freight or carrier cost is recorded. l_extendedprice is the goods' value, not shipping cost. |
| l17 | Which shipping mode should we recommend for fragile parts? | **MISSING_DATA** | Shipping mode is lineitem.l_shipmode, but nothing marks parts as fragile (p_type and p_container describe finish, material and packaging), and no damage or breakage outcomes exist to base a recommendation on. |
| l18 | In 1996, which five nations' customers paid the most in total once tax is included? | **ANSWERABLE** | Amount paid with tax is the order total orders.o_totalprice, which the glossary (Order value; Charge) and spec 4.2.3 define as the sum of line charges including tax. Sum it per customer nation for orders with o_orderdate in 1996 and take the top 5. Stored and computed totals agree by definition. I rejected filtering by ship date, since payment attaches to the order. |
| l19 | Which nation generated the most revenue in 1996? | **AMBIGUOUS** | Revenue is l_extendedprice*(1-l_discount) (glossary: Revenue), but 'nation' could be the customer's nation (customer.c_nationkey) or the supplier's nation (supplier.s_nationkey). Each line item has both, and they rank nations differently. |
| l20 | What were the most common reasons customers gave for returning items in 1995? | **MISSING_DATA** | lineitem.l_returnflag = 'R' marks returned items, but no return reason is stored. l_comment is generated filler text (glossary: Free text). |

## Evidence

### l01: AMBIGUOUS

> What is the average price of a part?

Links: ✓ "average" → shape `aggregation`<br>✓ "part" → part<br>✓ "price" → part.p_retailprice OR partsupp.ps_supplycost OR lineitem.l_extendedprice, lineitem.l_discount, lineitem.l_quantity

- Reading 1: price = the part's list price, averaged over all parts (AVG p_retailprice). Links: ✓ "average" → shape `aggregation`<br>✓ "price of a part" → part.p_retailprice
- Reading 2: price = the supply cost suppliers charge per unit (AVG ps_supplycost). Links: ✓ "average" → shape `aggregation`<br>✓ "price of a part" → partsupp.ps_supplycost
- Reading 3: price = realized unit selling price on line items, l_extendedprice*(1-l_discount)/l_quantity. Links: ✓ "average" → shape `aggregation`<br>✓ "price of a part" → lineitem.l_extendedprice, lineitem.l_discount, lineitem.l_quantity


### l02: MISSING_DATA

> What is the average customer satisfaction rating per market segment?

Links: ✓ "average" → shape `aggregation`<br>✓ "customer satisfaction rating" → MISSING: customer satisfaction rating<br>✓ "per market segment" → customer.c_mktsegment<br>✓ "per" → shape `aggregation`

- Missing concept: **customer satisfaction rating**. Closest: customer.c_comment, lineitem.l_returnflag. no rating, survey or feedback column exists; comments are random generated text

### l03: MISSING_DATA

> Which clerks exceeded their quarterly sales targets in 1996?

Links: ✓ "clerks" → orders.o_clerk<br>✓ "quarterly sales targets" → MISSING: per-clerk quarterly sales target<br>✓ "in 1996" → orders.o_orderdate = `1996`

- Missing concept: **per-clerk quarterly sales target**. Closest: orders.o_clerk, orders.o_totalprice. no target or quota data exists for clerks; only the actual orders they handled

### l04: AMBIGUOUS

> What was the average number of orders per customer in 1995?

Links: ✓ "average number of" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "per customer" → customer<br>✓ "in 1995" → orders.o_orderdate = `1995`

- Reading 1: average over customers who placed at least one order in 1995 (orders only, no join). Links: ✓ "average number of" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "per customer" → orders.o_custkey<br>✓ "in 1995" → orders.o_orderdate = `1995`
- Reading 2: average over all customers in the customer table, counting zero for those with no 1995 orders. Links: ✓ "average number of" → shape `aggregation`<br>✓ "orders" → orders<br>✓ "per customer" → customer<br>✓ "in 1995" → orders.o_orderdate = `1995`


### l05: ANSWERABLE

> Which 10 parts of size 50 have the lowest total available quantity across all suppliers?

Links: ✓ "10" → shape `ranking`<br>✓ "lowest" → shape `ranking`<br>✓ "parts" → part<br>✓ "size 50" → part.p_size = `50`<br>✓ "total" → shape `aggregation`<br>✓ "available quantity" → partsupp.ps_availqty<br>✓ "across all suppliers" → partsupp


### l06: MISSING_DATA

> What is the population of GERMANY?

Links: ✓ "population" → MISSING: country population<br>✓ "GERMANY" → nation.n_name = `GERMANY`

- Missing concept: **country population**. Closest: nation.n_name, nation.n_comment. the nation table has no population or demographic attribute

### l07: ANSWERABLE

> In which countries is the average account balance of customers higher than the overall average for all customers?

Links: ✓ "countries" → nation.n_name<br>✓ "average account balance" → customer.c_acctbal<br>✓ "average" → shape `aggregation`<br>✓ "customers" → customer<br>✓ "higher than the overall average" → shape `vs_aggregate`


### l08: AMBIGUOUS

> Which customers placed large orders in 1997?

Links: ✓ "customers" → customer<br>✓ "large orders" → orders.o_totalprice OR lineitem.l_quantity<br>✓ "in 1997" → orders.o_orderdate = `1997`

- Reading 1: large = orders with a high total value (o_totalprice above some threshold). Links: ✓ "customers" → customer<br>✓ "large orders" → orders.o_totalprice<br>✓ "in 1997" → orders.o_orderdate = `1997`
- Reading 2: large = orders with a high total quantity (sum of l_quantity above some threshold). Links: ✓ "customers" → customer<br>✓ "large orders" → lineitem.l_quantity<br>✓ "in 1997" → orders.o_orderdate = `1997`


### l09: MISSING_DATA

> What is the average weight of parts shipped by TRUCK?

Links: ✓ "average" → shape `aggregation`<br>✓ "weight" → MISSING: part weight<br>✓ "parts" → part<br>✓ "shipped by TRUCK" → lineitem.l_shipmode = `TRUCK`

- Missing concept: **part weight**. Closest: part.p_size, part.p_container, lineitem.l_quantity. no weight column exists; p_size is an integer size 1-50, not a weight

### l10: ANSWERABLE

> For line items shipped between 1993 and 1997 to customers in ASIA, how did the average time from shipment to receipt change each year?

Links: ✓ "line items" → lineitem<br>✓ "shipped between 1993 and 1997" → lineitem.l_shipdate = `1993..1997`<br>✓ "customers" → customer<br>✓ "ASIA" → region.r_name = `ASIA`<br>✓ "average" → shape `aggregation`<br>✓ "time from shipment to receipt" → lineitem.l_receiptdate, lineitem.l_shipdate<br>✓ "change each year" → shape `time_trend`


### l11: ANSWERABLE

> How did the number of late deliveries from suppliers in INDIA change year by year for items received between 1993 and 1997?

Links: ✓ "number of" → shape `aggregation`<br>✓ "late deliveries" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "suppliers" → supplier<br>✓ "INDIA" → nation.n_name = `INDIA`<br>✓ "change year by year" → shape `time_trend`<br>✓ "items" → lineitem<br>✓ "received between 1993 and 1997" → lineitem.l_receiptdate = `1993..1997`


### l12: OFF_TOPIC

> Who won the FIFA World Cup in 1998?

Links: -


### l13: MISSING_DATA

> How did the available quantity of Brand#23 parts change month by month during 1997?

Links: ✓ "available quantity … change month by month" → MISSING: dated history of available quantity<br>✓ "Brand#23" → part.p_brand = `Brand#23`<br>✓ "parts" → part

- Missing concept: **dated history of available quantity**. Closest: partsupp.ps_availqty. ps_availqty is a single undated snapshot per part and supplier; no inventory history or dates exist

### l14: MISSING_DATA

> Which cities had the most late deliveries in 1996?

Links: ✓ "cities" → MISSING: city<br>✓ "the most" → shape `ranking`<br>✓ "late deliveries" → lineitem.l_receiptdate, lineitem.l_commitdate<br>✓ "in 1996" → lineitem.l_receiptdate = `1996`

- Missing concept: **city**. Closest: customer.c_address, supplier.s_address, nation.n_name. addresses are random v-strings with no city component; geography stops at nation

### l15: AMBIGUOUS

> How many line items did we have in March 1996?

Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "March 1996" → lineitem.l_shipdate = `1996-03` OR orders.o_orderdate OR lineitem.l_receiptdate

- Reading 1: line items whose order was placed in March 1996 (o_orderdate). Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "March 1996" → orders.o_orderdate = `1996-03`
- Reading 2: line items shipped in March 1996 (l_shipdate). Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "March 1996" → lineitem.l_shipdate = `1996-03`
- Reading 3: line items received in March 1996 (l_receiptdate). Links: ✓ "How many" → shape `aggregation`<br>✓ "line items" → lineitem<br>✓ "March 1996" → lineitem.l_receiptdate = `1996-03`


### l16: MISSING_DATA

> What was the total freight cost paid to carriers for AIR shipments in 1996?

Links: ✓ "total" → shape `aggregation`<br>✓ "freight cost paid to carriers" → MISSING: freight / carrier shipping cost<br>✓ "AIR shipments" → lineitem.l_shipmode = `AIR`<br>✓ "in 1996" → lineitem.l_shipdate = `1996`

- Missing concept: **freight / carrier shipping cost**. Closest: lineitem.l_shipmode, lineitem.l_extendedprice. no shipping cost or carrier data exists; l_extendedprice is the value of the goods

### l17: MISSING_DATA

> Which shipping mode should we recommend for fragile parts?

Links: ✓ "shipping mode" → lineitem.l_shipmode<br>✓ "fragile parts" → MISSING: part fragility

- Missing concept: **part fragility**. Closest: part.p_type, part.p_container. no fragility attribute and no damage or breakage data exists

### l18: ANSWERABLE

> In 1996, which five nations' customers paid the most in total once tax is included?

Links: ✓ "In 1996" → orders.o_orderdate = `1996`<br>✓ "five … the most" → shape `ranking`<br>✓ "nations'" → nation.n_name<br>✓ "customers" → customer<br>✓ "paid … once tax is included" → orders.o_totalprice<br>✓ "in total" → shape `aggregation`


### l19: AMBIGUOUS

> Which nation generated the most revenue in 1996?

Links: ✓ "nation" → nation.n_name, customer.c_nationkey OR nation.n_name, supplier.s_nationkey<br>✓ "the most" → shape `ranking`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "in 1996" → orders.o_orderdate = `1996`

- Reading 1: nation = the customer's nation (where revenue is earned from). Links: ✓ "nation" → nation.n_name, customer.c_nationkey<br>✓ "the most" → shape `ranking`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "in 1996" → orders.o_orderdate = `1996`
- Reading 2: nation = the supplier's nation (which suppliers' sales generated the revenue). Links: ✓ "nation" → nation.n_name, supplier.s_nationkey<br>✓ "the most" → shape `ranking`<br>✓ "revenue" → lineitem.l_extendedprice, lineitem.l_discount<br>✓ "in 1996" → orders.o_orderdate = `1996`


### l20: MISSING_DATA

> What were the most common reasons customers gave for returning items in 1995?

Links: ✓ "most common" → shape `ranking`<br>✓ "reasons customers gave for returning items" → MISSING: return reason<br>✓ "in 1995" → lineitem.l_receiptdate = `1995`

- Missing concept: **return reason**. Closest: lineitem.l_returnflag, lineitem.l_comment. only a returned/accepted flag exists; no reason codes or feedback are recorded
