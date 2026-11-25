# TPC-H business glossary

Written for this project to give the question generator and the judges shared business definitions. Facts about value generation come from the TPC-H specification v3.0.1, clause 4.2.3 (extracted next to this file under `spec/`, when downloaded). Definitions marked *convention* are this project's choices.

## The business

TPC-H portrays a **wholesale supplier** that sells parts to customers worldwide. Suppliers supply parts (with a cost and an available quantity per part and supplier), customers place orders, and each order has one to seven line items, each a quantity of one part from one supplier. Customers and suppliers belong to a nation, and every nation belongs to one of five regions.

## Money

| Term | Definition |
|---|---|
| **Gross value of a line** | `l_extendedprice` = quantity × the part's retail price. Before discount and tax. |
| **Discount** | `l_discount`, a fraction between 0.00 and 0.10 (0.05 = 5%). |
| **Tax** | `l_tax`, a fraction between 0.00 and 0.08. |
| **Revenue** (*convention*) | `l_extendedprice × (1 − l_discount)`: the discounted value of line items, without tax. "Sales" means the same. |
| **Charge** | `l_extendedprice × (1 − l_discount) × (1 + l_tax)`: what the customer pays for a line, with tax. |
| **Order value / order total** | `o_totalprice` = the sum of the charges of the order's line items (spec clause 4.2.3). Includes tax and discount. |
| **Supply cost** | `ps_supplycost`: what one unit of a part costs from a given supplier. |
| **Profit** (*convention*) | `l_extendedprice × (1 − l_discount) − ps_supplycost × l_quantity`, using the supply cost of the line's part and supplier. |
| **Account balance** | `c_acctbal` / `s_acctbal`; can be negative. |

## Dates and fulfilment

| Term | Definition |
|---|---|
| **Order date** | `o_orderdate`: when the order was placed (1992-01-01 to 1998-08-02 in this data). |
| **Ship date / commit date / receipt date** | `l_shipdate`: when the line was shipped; `l_commitdate`: the date promised to the customer; `l_receiptdate`: when the customer received it. |
| **Late delivery** (*convention*) | A line item received after its commit date: `l_receiptdate > l_commitdate`. |
| **Days late** (*convention*) | `l_receiptdate − l_commitdate`, counted only for late deliveries. |
| **Shipping time / transit time** (*convention*) | `l_receiptdate − l_shipdate`. |
| **The data's "current date"** | The spec generates status codes as of **1995-06-17** (its CURRENTDATE). Line and order statuses describe the business as of that date, not as of the latest order. |

## Coded columns

| Column | Values | Meaning (spec clause 4.2.3) |
|---|---|---|
| `l_returnflag` | `R`, `A`, `N` | Items received by 1995-06-17 get `R` or `A` at random; later items get `N`. By convention **R = returned**, **A = accepted (not returned)**, **N = not yet received** as of 1995-06-17. |
| `l_linestatus` | `O`, `F` | `O` (open) if shipped after 1995-06-17; `F` (fulfilled) otherwise. |
| `o_orderstatus` | `F`, `O`, `P` | `F` if all of the order's lines are `F`; `O` if all are `O`; `P` (partially fulfilled) otherwise. |
| `o_orderpriority` | `1-URGENT` … `5-LOW` | The order's priority. |
| `o_shippriority` | always `0` | Set to 0 for every order by the generator, so it carries no information. |
| `l_shipmode` | `AIR`, `REG AIR`, `RAIL`, `SHIP`, `TRUCK`, `MAIL`, `FOB` | How the line was shipped. |
| `l_shipinstruct` | `DELIVER IN PERSON`, `COLLECT COD`, `TAKE BACK RETURN`, `NONE` | Shipping instruction. |
| `c_mktsegment` | `AUTOMOBILE`, `BUILDING`, `FURNITURE`, `HOUSEHOLD`, `MACHINERY` | The customer's market segment. |

## Parts

| Term | Definition |
|---|---|
| **Part type** | `p_type`: three words, e.g. `STANDARD POLISHED BRASS`. The last word is the material (TIN, NICKEL, BRASS, STEEL, COPPER). |
| **Container** | `p_container`: size + kind, e.g. `SM BOX`, `JUMBO PKG`. |
| **Brand / manufacturer** | `p_brand` (`Brand#MN`) belongs to manufacturer `p_mfgr` (`Manufacturer#M`). |
| **Size** | `p_size`, an integer from 1 to 50. |
| **Available quantity** | `ps_availqty`: units a supplier has available of a part. |

## Relative dates (*convention*)

Relative phrases ("last quarter", "this year") are resolved against the configured **time anchor**: by default the latest order date in the data (1998-08-02). The exact ranges are printed in each run's brief. When the anchor is off, relative phrases have no fixed meaning.

## Free text

`*_comment`, `c_address`, `s_address` and phone numbers hold generated text with no business meaning beyond identification. Phone numbers start with a country code derived from the nation.
