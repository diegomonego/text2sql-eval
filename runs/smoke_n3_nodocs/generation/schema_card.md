# Schema card

Engine: duckdb 2.0.1. 8 tables, 61 columns. Discovered from the database catalog and data at run time.

## customer (15,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `c_custkey` | BIGINT | 15,000 distinct; 1 to 15000 |  |  |
| `c_name` | VARCHAR | 15,000 distinct; length 18-18 | e.g. `Customer#000000001`, `Customer#000000002`, `Customer#000000003` |  |
| `c_address` | VARCHAR | 15,000 distinct; length 10-40 | e.g. `   5L06W67,Mw8G`, `  fb1LA6BKjWwc,DQMqKnUTlx88ugWRvAny8xcTv`, `  udI60hnJb0IMvB67xQFfkgamLpP2Bwynf5P` |  |
| `c_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `c_phone` | VARCHAR | 15,000 distinct; length 15-15 | e.g. `10-103-318-6809`, `10-109-430-5638`, `10-109-684-5601` |  |
| `c_acctbal` | DECIMAL(15,2) | 14,887 distinct; -999.95 to 9,999.72 |  |  |
| `c_mktsegment` | VARCHAR | 5 distinct; length 8-10 | values: `AUTOMOBILE`, `BUILDING`, `FURNITURE`, `HOUSEHOLD`, `MACHINERY` |  |
| `c_comment` | VARCHAR | 15,000 distinct; length 29-116 | e.g. ` Tiresias among the boldly regular pinto beans wake pending`, ` Tiresias poach after the quickly special foxes. c`, ` about the carefully ironic pinto beans. accoun` |  |

## lineitem (600,572 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `l_orderkey` | BIGINT | 150,000 distinct; 1 to 600000 |  |  |
| `l_partkey` | BIGINT | 20,000 distinct; 1 to 20000 |  |  |
| `l_suppkey` | BIGINT | 1,000 distinct; 1 to 1000 |  |  |
| `l_linenumber` | BIGINT | 7 distinct; 1 to 7 | values: `1`, `2`, `3`, `4`, `5`, `6`, `7` |  |
| `l_quantity` | DECIMAL(15,2) | 50 distinct; 1.00 to 50.00 |  |  |
| `l_extendedprice` | DECIMAL(15,2) | 130,792 distinct; 901.00 to 95,949.50 |  |  |
| `l_discount` | DECIMAL(15,2) | 11 distinct; 0.00 to 0.10 |  |  |
| `l_tax` | DECIMAL(15,2) | 9 distinct; 0.00 to 0.08 | values: `0.0`, `0.01`, `0.02`, `0.03`, `0.04`, `0.05`, `0.06`, `0.07`, `0.08` |  |
| `l_returnflag` | VARCHAR | 3 distinct; length 1-1 | values: `A`, `N`, `R` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `l_linestatus` | VARCHAR | 2 distinct; length 1-1 | values: `F`, `O` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `l_shipdate` | DATE | 2,525 distinct; 1992-01-03 to 1998-12-01 |  |  |
| `l_commitdate` | DATE | 2,466 distinct; 1992-01-31 to 1998-10-31 |  |  |
| `l_receiptdate` | DATE | 2,547 distinct; 1992-01-04 to 1998-12-27 |  |  |
| `l_shipinstruct` | VARCHAR | 4 distinct; length 4-17 | values: `COLLECT COD`, `DELIVER IN PERSON`, `NONE`, `TAKE BACK RETURN` |  |
| `l_shipmode` | VARCHAR | 7 distinct; length 3-7 | values: `AIR`, `FOB`, `MAIL`, `RAIL`, `REG AIR`, `SHIP`, `TRUCK` |  |
| `l_comment` | VARCHAR | 538,684 distinct; length 10-43 | e.g. ` Tiresias `, ` Tiresias above the stealthily p`, ` Tiresias across the bold re` |  |

## nation (25 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `n_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `n_name` | VARCHAR | 25 distinct; length 4-14 | values: `ALGERIA`, `ARGENTINA`, `BRAZIL`, `CANADA`, `CHINA`, `EGYPT`, `ETHIOPIA`, `FRANCE`, `GERMANY`, `INDIA`, `INDONESIA`, `IRAN`, `IRAQ`, `JAPAN`, `JORDAN`, `KENYA`, `MOROCCO`, `MOZAMBIQUE`, `PERU`, `ROMANIA`, `RUSSIA`, `SAUDI ARABIA`, `UNITED KINGDOM`, `UNITED STATES`, `VIETNAM` |  |
| `n_regionkey` | INTEGER | 5 distinct; 0 to 4 | values: `0`, `1`, `2`, `3`, `4` |  |
| `n_comment` | VARCHAR | 25 distinct; length 31-114 | values: ` haggle. carefully final deposits detect slyly agai`, ` pending excuses haggle furiously deposits. pending, express pinto beans wake fluffily past t`, ` requests against the platelets use never according to the quickly regular pint`, ` slyly express asymptotes. regular deposits haggle slyly. carefully ironic hockey players sleep blithely. carefull`, `al foxes promise slyly according to the regular accounts. bold requests alon`, `c dependencies. furiously express notornis sleep slyly regular accounts. ideas sleep. depos`, `eans boost carefully special requests. accounts are. carefull`, `eas hang ironic, silent packages. slyly regular packages are furiously over the tithes. fluffily bold`, `efully alongside of the slyly final dependencies. `, `hely enticingly express accounts. even, final `, `ic deposits are blithely about the carefully regular pa`, `l platelets. regular accounts x-ray: unusual, regular acco`, `nic deposits boost atop the quickly final requests? quickly regula`, `ously. final, express gifts cajole a`, `platelets. blithely pending dependencies use fluffily across the even pinto beans. carefully silent accoun`, `refully final requests. regular, ironi`, `rns. blithely bold courts among the closely regular packages use furiously bold platelets?`, `s. ironic, unusual asymptotes wake blithely r`, `ss excuses cajole slyly across the packages. deposits print aroun`, `ts. silent requests haggle. closely express packages sleep across the blithely`, `ular asymptotes are about the furious multipliers. express dependencies nag above the ironically ironic account`, `ven packages wake quickly. regu`, `y above the carefully unusual theodolites. final dugouts are quickly across the furiously regular d`, `y alongside of the pending deposits. carefully special packages are about the ironic forges. slyly special `, `y final packages. slow foxes cajole quickly. quickly silent platelets breach ironic accounts. unusual pinto be` |  |

## orders (150,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `o_orderkey` | BIGINT | 150,000 distinct; 1 to 600000 |  |  |
| `o_custkey` | BIGINT | 10,000 distinct; 1 to 14999 |  |  |
| `o_orderstatus` | VARCHAR | 3 distinct; length 1-1 | values: `F`, `O`, `P` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `o_totalprice` | DECIMAL(15,2) | 149,565 distinct; 833.40 to 479,129.21 |  |  |
| `o_orderdate` | DATE | 2,406 distinct; 1992-01-01 to 1998-08-02 |  |  |
| `o_orderpriority` | VARCHAR | 5 distinct; length 5-15 | values: `1-URGENT`, `2-HIGH`, `3-MEDIUM`, `4-NOT SPECIFIED`, `5-LOW` |  |
| `o_clerk` | VARCHAR | 1,000 distinct; length 15-15 | e.g. `Clerk#000000001`, `Clerk#000000002`, `Clerk#000000003` |  |
| `o_shippriority` | INTEGER | 1 distinct; 0 to 0 | values: `0` | constant in this data |
| `o_comment` | VARCHAR | 149,770 distinct; length 19-78 | e.g. ` Tiresias about the blithely ironic a`, ` Tiresias above the carefully ironic packages nag about the pend`, ` Tiresias use deposits. carefully express deposits integrat` |  |

## part (20,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `p_partkey` | BIGINT | 20,000 distinct; 1 to 20000 |  |  |
| `p_name` | VARCHAR | 20,000 distinct; length 21-47 | e.g. `almond antique metallic honeydew green`, `almond antique orange white violet`, `almond aquamarine frosted tomato green` |  |
| `p_mfgr` | VARCHAR | 5 distinct; length 14-14 | values: `Manufacturer#1`, `Manufacturer#2`, `Manufacturer#3`, `Manufacturer#4`, `Manufacturer#5` |  |
| `p_brand` | VARCHAR | 25 distinct; length 8-8 | values: `Brand#11`, `Brand#12`, `Brand#13`, `Brand#14`, `Brand#15`, `Brand#21`, `Brand#22`, `Brand#23`, `Brand#24`, `Brand#25`, `Brand#31`, `Brand#32`, `Brand#33`, `Brand#34`, `Brand#35`, `Brand#41`, `Brand#42`, `Brand#43`, `Brand#44`, `Brand#45`, `Brand#51`, `Brand#52`, `Brand#53`, `Brand#54`, `Brand#55` |  |
| `p_type` | VARCHAR | 150 distinct; length 16-25 | e.g. `ECONOMY ANODIZED BRASS`, `ECONOMY ANODIZED COPPER`, `ECONOMY ANODIZED NICKEL` |  |
| `p_size` | INTEGER | 50 distinct; 1 to 50 |  |  |
| `p_container` | VARCHAR | 40 distinct; length 6-10 | e.g. `JUMBO BAG`, `JUMBO BOX`, `JUMBO CAN` |  |
| `p_retailprice` | DECIMAL(15,2) | 2,899 distinct; 901.00 to 1,918.99 |  |  |
| `p_comment` | VARCHAR | 17,482 distinct; length 5-22 | e.g. ` Tiresias boost a`, ` Tiresias. furiou`, ` Tiresias. quickly bus` |  |

## partsupp (80,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ps_partkey` | BIGINT | 20,000 distinct; 1 to 20000 |  |  |
| `ps_suppkey` | BIGINT | 1,000 distinct; 1 to 1000 |  |  |
| `ps_availqty` | BIGINT | 9,996 distinct; 1 to 9999 |  |  |
| `ps_supplycost` | DECIMAL(15,2) | 54,983 distinct; 1.01 to 999.99 |  |  |
| `ps_comment` | VARCHAR | 79,991 distinct; length 49-198 | e.g. ` Tiresias haggle quickly upon the special instructions. blithely pending platelets across the bold`, ` Tiresias print carefully regular requests. ironic accounts use quickly along the furiously even pearls. packages sleep furiously unusual asymptotes. furiously unusual hockey playe`, ` Tiresias. carefully final instructions along the blithely re` |  |

## region (5 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `r_regionkey` | INTEGER | 5 distinct; 0 to 4 | values: `0`, `1`, `2`, `3`, `4` |  |
| `r_name` | VARCHAR | 5 distinct; length 4-11 | values: `AFRICA`, `AMERICA`, `ASIA`, `EUROPE`, `MIDDLE EAST` |  |
| `r_comment` | VARCHAR | 5 distinct; length 31-115 | values: `ges. thinly even pinto beans ca`, `hs use ironic, even requests. s`, `lar deposits. blithely final packages cajole. regular waters are final requests. regular accounts are according to `, `ly final courts cajole furiously final excuse`, `uickly special accounts cajole carefully blithely close requests. carefully final asymptotes haggle furiousl` |  |

## supplier (1,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `s_suppkey` | BIGINT | 1,000 distinct; 1 to 1000 |  |  |
| `s_name` | VARCHAR | 1,000 distinct; length 18-18 | e.g. `Supplier#000000001`, `Supplier#000000002`, `Supplier#000000003` |  |
| `s_address` | VARCHAR | 1,000 distinct; length 10-40 | e.g. ` 0L8yoIwSCP4EJyESI 6bVH9k`, ` 2mQLQsVJ8WLBSnl0R bXrcyTgqXKrplgxb`, ` 3kCm2eN3Jra2UzvWWBm,P04b` |  |
| `s_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `s_phone` | VARCHAR | 1,000 distinct; length 15-15 | e.g. `10-108-564-6160`, `10-119-372-1062`, `10-178-678-7353` |  |
| `s_acctbal` | DECIMAL(15,2) | 999 distinct; -966.20 to 9,993.46 |  |  |
| `s_comment` | VARCHAR | 1,000 distinct; length 25-100 | e.g. ` according to the bravely quick dolphins. deposit`, ` according to the ironic packages.`, ` accounts detect slyly bo` |  |

## Joins

No foreign keys are declared; these were inferred from column names and confirmed against the data.

- `customer.c_nationkey` -> `nation.n_nationkey`
- `lineitem.l_orderkey` -> `orders.o_orderkey`
- `lineitem.l_partkey` -> `part.p_partkey`
- `lineitem.l_suppkey` -> `supplier.s_suppkey`
- `nation.n_regionkey` -> `region.r_regionkey`
- `orders.o_custkey` -> `customer.c_custkey`
- `partsupp.ps_partkey` -> `part.p_partkey`
- `partsupp.ps_suppkey` -> `supplier.s_suppkey`
- `supplier.s_nationkey` -> `nation.n_nationkey`
