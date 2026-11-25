# Schema card

Engine: duckdb 2.0.1. 8 tables, 61 columns. Discovered from the database catalog and data at run time.

## customer (1,500 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `c_custkey` | BIGINT | 1,500 distinct; 1 to 1500 |  |  |
| `c_name` | VARCHAR | 1,500 distinct; length 18-18 | e.g. `Customer#000000001`, `Customer#000000002`, `Customer#000000003` |  |
| `c_address` | VARCHAR | 1,500 distinct; length 10-40 | e.g. ` ,cIZ,06Kg`, ` 3QsPgbVLZ`, ` 3b8K2YhfbGDJOpSAUrvq82MnkhHBdwL` |  |
| `c_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `c_phone` | VARCHAR | 1,500 distinct; length 15-15 | e.g. `10-109-430-5638`, `10-203-771-2219`, `10-209-317-6929` |  |
| `c_acctbal` | DECIMAL(15,2) | 1,499 distinct; -994.79 to 9,987.71 |  |  |
| `c_mktsegment` | VARCHAR | 5 distinct; length 8-10 | values: `AUTOMOBILE`, `BUILDING`, `FURNITURE`, `HOUSEHOLD`, `MACHINERY` |  |
| `c_comment` | VARCHAR | 1,500 distinct; length 29-116 | e.g. ` about the carefully ironic pinto beans. accoun`, ` according to the carefully bold dependencies use boldly slyly express deposits. car`, ` according to the slyly bold accounts. ` |  |

## lineitem (60,175 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `l_orderkey` | BIGINT | 15,000 distinct; 1 to 60000 |  |  |
| `l_partkey` | BIGINT | 2,000 distinct; 1 to 2000 |  |  |
| `l_suppkey` | BIGINT | 100 distinct; 1 to 100 |  |  |
| `l_linenumber` | BIGINT | 7 distinct; 1 to 7 | values: `1`, `2`, `3`, `4`, `5`, `6`, `7` |  |
| `l_quantity` | DECIMAL(15,2) | 50 distinct; 1.00 to 50.00 |  |  |
| `l_extendedprice` | DECIMAL(15,2) | 35,921 distinct; 904.00 to 94,949.50 |  |  |
| `l_discount` | DECIMAL(15,2) | 11 distinct; 0.00 to 0.10 |  |  |
| `l_tax` | DECIMAL(15,2) | 9 distinct; 0.00 to 0.08 | values: `0.0`, `0.01`, `0.02`, `0.03`, `0.04`, `0.05`, `0.06`, `0.07`, `0.08` |  |
| `l_returnflag` | VARCHAR | 3 distinct; length 1-1 | values: `A`, `N`, `R` | coded: meaning needs docs |
| `l_linestatus` | VARCHAR | 2 distinct; length 1-1 | values: `F`, `O` | coded: meaning needs docs |
| `l_shipdate` | DATE | 2,518 distinct; 1992-01-04 to 1998-11-29 |  |  |
| `l_commitdate` | DATE | 2,460 distinct; 1992-02-02 to 1998-10-28 |  |  |
| `l_receiptdate` | DATE | 2,529 distinct; 1992-01-09 to 1998-12-25 |  |  |
| `l_shipinstruct` | VARCHAR | 4 distinct; length 4-17 | values: `COLLECT COD`, `DELIVER IN PERSON`, `NONE`, `TAKE BACK RETURN` |  |
| `l_shipmode` | VARCHAR | 7 distinct; length 3-7 | values: `AIR`, `FOB`, `MAIL`, `RAIL`, `REG AIR`, `SHIP`, `TRUCK` |  |
| `l_comment` | VARCHAR | 58,616 distinct; length 10-43 | e.g. ` Tiresias `, ` Tiresias across the bold re`, ` Tiresias alongside of the carefully spec` |  |

## nation (25 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `n_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `n_name` | VARCHAR | 25 distinct; length 4-14 | values: `ALGERIA`, `ARGENTINA`, `BRAZIL`, `CANADA`, `CHINA`, `EGYPT`, `ETHIOPIA`, `FRANCE`, `GERMANY`, `INDIA`, `INDONESIA`, `IRAN`, `IRAQ`, `JAPAN`, `JORDAN`, `KENYA`, `MOROCCO`, `MOZAMBIQUE`, `PERU`, `ROMANIA`, `RUSSIA`, `SAUDI ARABIA`, `UNITED KINGDOM`, `UNITED STATES`, `VIETNAM` |  |
| `n_regionkey` | INTEGER | 5 distinct; 0 to 4 | values: `0`, `1`, `2`, `3`, `4` |  |
| `n_comment` | VARCHAR | 25 distinct; length 31-114 | values: ` haggle. carefully final deposits detect slyly agai`, ` pending excuses haggle furiously deposits. pending, express pinto beans wake fluffily past t`, ` requests against the platelets use never according to the quickly regular pint`, ` slyly express asymptotes. regular deposits haggle slyly. carefully ironic hockey players sleep blithely. carefull`, `al foxes promise slyly according to the regular accounts. bold requests alon`, `c dependencies. furiously express notornis sleep slyly regular accounts. ideas sleep. depos`, `eans boost carefully special requests. accounts are. carefull`, `eas hang ironic, silent packages. slyly regular packages are furiously over the tithes. fluffily bold`, `efully alongside of the slyly final dependencies. `, `hely enticingly express accounts. even, final `, `ic deposits are blithely about the carefully regular pa`, `l platelets. regular accounts x-ray: unusual, regular acco`, `nic deposits boost atop the quickly final requests? quickly regula`, `ously. final, express gifts cajole a`, `platelets. blithely pending dependencies use fluffily across the even pinto beans. carefully silent accoun`, `refully final requests. regular, ironi`, `rns. blithely bold courts among the closely regular packages use furiously bold platelets?`, `s. ironic, unusual asymptotes wake blithely r`, `ss excuses cajole slyly across the packages. deposits print aroun`, `ts. silent requests haggle. closely express packages sleep across the blithely`, `ular asymptotes are about the furious multipliers. express dependencies nag above the ironically ironic account`, `ven packages wake quickly. regu`, `y above the carefully unusual theodolites. final dugouts are quickly across the furiously regular d`, `y alongside of the pending deposits. carefully special packages are about the ironic forges. slyly special `, `y final packages. slow foxes cajole quickly. quickly silent platelets breach ironic accounts. unusual pinto be` |  |

## orders (15,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `o_orderkey` | BIGINT | 15,000 distinct; 1 to 60000 |  |  |
| `o_custkey` | BIGINT | 1,000 distinct; 1 to 1499 |  |  |
| `o_orderstatus` | VARCHAR | 3 distinct; length 1-1 | values: `F`, `O`, `P` | coded: meaning needs docs |
| `o_totalprice` | DECIMAL(15,2) | 14,996 distinct; 874.89 to 466,001.28 |  |  |
| `o_orderdate` | DATE | 2,401 distinct; 1992-01-01 to 1998-08-02 |  |  |
| `o_orderpriority` | VARCHAR | 5 distinct; length 5-15 | values: `1-URGENT`, `2-HIGH`, `3-MEDIUM`, `4-NOT SPECIFIED`, `5-LOW` |  |
| `o_clerk` | VARCHAR | 1,000 distinct; length 15-15 | e.g. `Clerk#000000001`, `Clerk#000000002`, `Clerk#000000003` |  |
| `o_shippriority` | INTEGER | 1 distinct; 0 to 0 | values: `0` | constant in this data |
| `o_comment` | VARCHAR | 14,995 distinct; length 19-78 | e.g. ` about the accounts. slyly express accounts wa`, ` about the blithely ironic requests. fluffily ironic `, ` about the blithely pending theod` |  |

## part (2,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `p_partkey` | BIGINT | 2,000 distinct; 1 to 2000 |  |  |
| `p_name` | VARCHAR | 2,000 distinct; length 23-46 | e.g. `almond aquamarine mint misty red`, `almond azure drab ghost mint`, `almond bisque steel rosy burlywood` |  |
| `p_mfgr` | VARCHAR | 5 distinct; length 14-14 | values: `Manufacturer#1`, `Manufacturer#2`, `Manufacturer#3`, `Manufacturer#4`, `Manufacturer#5` |  |
| `p_brand` | VARCHAR | 25 distinct; length 8-8 | values: `Brand#11`, `Brand#12`, `Brand#13`, `Brand#14`, `Brand#15`, `Brand#21`, `Brand#22`, `Brand#23`, `Brand#24`, `Brand#25`, `Brand#31`, `Brand#32`, `Brand#33`, `Brand#34`, `Brand#35`, `Brand#41`, `Brand#42`, `Brand#43`, `Brand#44`, `Brand#45`, `Brand#51`, `Brand#52`, `Brand#53`, `Brand#54`, `Brand#55` |  |
| `p_type` | VARCHAR | 150 distinct; length 16-25 | e.g. `ECONOMY ANODIZED BRASS`, `ECONOMY ANODIZED COPPER`, `ECONOMY ANODIZED NICKEL` |  |
| `p_size` | INTEGER | 50 distinct; 1 to 50 |  |  |
| `p_container` | VARCHAR | 40 distinct; length 6-10 | e.g. `JUMBO BAG`, `JUMBO BOX`, `JUMBO CAN` |  |
| `p_retailprice` | DECIMAL(15,2) | 1,099 distinct; 901.00 to 1,900.99 |  |  |
| `p_comment` | VARCHAR | 1,959 distinct; length 5-22 | e.g. ` about the furio`, ` above the i`, ` above the silent p` |  |

## partsupp (8,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ps_partkey` | BIGINT | 2,000 distinct; 1 to 2000 |  |  |
| `ps_suppkey` | BIGINT | 100 distinct; 1 to 100 |  |  |
| `ps_availqty` | BIGINT | 5,497 distinct; 3 to 9998 |  |  |
| `ps_supplycost` | DECIMAL(15,2) | 7,665 distinct; 1.05 to 999.99 |  |  |
| `ps_comment` | VARCHAR | 8,000 distinct; length 49-198 | e.g. ` about the instructions. carefully final platelets cajole carefully furiously regular requests. carefully regular theodolites along the carefully regular pinto beans haggle about `, ` about the permanent, even theodolites. even, ironic ideas wake. quickly special `, ` about the silent ideas. fluffily final requests impress. slyly final requests wake carefully about the slyly express foxes. slyly regular warthogs sleep fur` |  |

## region (5 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `r_regionkey` | INTEGER | 5 distinct; 0 to 4 | values: `0`, `1`, `2`, `3`, `4` |  |
| `r_name` | VARCHAR | 5 distinct; length 4-11 | values: `AFRICA`, `AMERICA`, `ASIA`, `EUROPE`, `MIDDLE EAST` |  |
| `r_comment` | VARCHAR | 5 distinct; length 31-115 | values: `ges. thinly even pinto beans ca`, `hs use ironic, even requests. s`, `lar deposits. blithely final packages cajole. regular waters are final requests. regular accounts are according to `, `ly final courts cajole furiously final excuse`, `uickly special accounts cajole carefully blithely close requests. carefully final asymptotes haggle furiousl` |  |

## supplier (100 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `s_suppkey` | BIGINT | 100 distinct; 1 to 100 |  |  |
| `s_name` | VARCHAR | 100 distinct; length 18-18 | e.g. `Supplier#000000001`, `Supplier#000000002`, `Supplier#000000003` |  |
| `s_address` | VARCHAR | 100 distinct; length 10-40 | e.g. ` N kD4on9OM Ipw3,gf0JBoQDd7tgrzrddZ`, `01dEADIZoCULZXg`, `1KhUgZegwM3ua7dsYmekYBsK` |  |
| `s_nationkey` | INTEGER | 25 distinct; 0 to 24 |  |  |
| `s_phone` | VARCHAR | 100 distinct; length 15-15 | e.g. `10-470-144-1330`, `10-538-384-8460`, `10-620-939-2254` |  |
| `s_acctbal` | DECIMAL(15,2) | 100 distinct; -966.20 to 9,915.24 |  |  |
| `s_comment` | VARCHAR | 100 distinct; length 25-100 | e.g. ` across the furiously regular platelets wake even deposits. quickly express she`, ` even theodolites wake against the blithely fluffy packages`, ` final accounts. bold, final escapades must have to cajole about the special platelets. fu` |  |

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
