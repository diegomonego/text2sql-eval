# Schema card

Engine: duckdb 2.0.1. 24 tables, 425 columns. Discovered from the database catalog and data at run time.

## call_center (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `cc_call_center_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `cc_call_center_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `cc_rec_start_date` | DATE | 1 distinct; 1998-01-01 to 1998-01-01 | values: `1998-01-01` | constant in this data |
| `cc_rec_end_date` | DATE | 0 distinct; 1 nulls; None to None | values:  |  |
| `cc_closed_date_sk` | BIGINT | 0 distinct; 1 nulls; None to None | values:  |  |
| `cc_open_date_sk` | BIGINT | 1 distinct; 2450952 to 2450952 | values: `2450952` | constant in this data |
| `cc_name` | VARCHAR | 1 distinct; length 8-8 | values: `NY Metro` | constant in this data |
| `cc_class` | VARCHAR | 1 distinct; length 5-5 | values: `large` | constant in this data |
| `cc_employees` | BIGINT | 1 distinct; 2 to 2 | values: `2` | constant in this data |
| `cc_sq_ft` | BIGINT | 1 distinct; 1138 to 1138 | values: `1138` | constant in this data |
| `cc_hours` | VARCHAR | 1 distinct; length 7-7 | values: `8AM-4PM` | constant in this data |
| `cc_manager` | VARCHAR | 1 distinct; length 11-11 | values: `Bob Belcher` | constant in this data |
| `cc_mkt_id` | BIGINT | 1 distinct; 6 to 6 | values: `6` | constant in this data |
| `cc_mkt_class` | VARCHAR | 1 distinct; length 23-23 | values: `More than other authori` | constant in this data |
| `cc_mkt_desc` | VARCHAR | 1 distinct; length 59-59 | values: `Shared others could not count fully dollars. New members ca` | constant in this data |
| `cc_market_manager` | VARCHAR | 1 distinct; length 11-11 | values: `Julius Tran` | constant in this data |
| `cc_division` | BIGINT | 1 distinct; 3 to 3 | values: `3` | constant in this data |
| `cc_division_name` | VARCHAR | 1 distinct; length 3-3 | values: `pri` | constant in this data |
| `cc_company` | BIGINT | 1 distinct; 6 to 6 | values: `6` | constant in this data |
| `cc_company_name` | VARCHAR | 1 distinct; length 5-5 | values: `cally` | constant in this data |
| `cc_street_number` | VARCHAR | 1 distinct; length 3-3 | values: `730` | constant in this data |
| `cc_street_name` | VARCHAR | 1 distinct; length 8-8 | values: `Ash Hill` | constant in this data |
| `cc_street_type` | VARCHAR | 1 distinct; length 9-9 | values: `Boulevard` | constant in this data |
| `cc_suite_number` | VARCHAR | 1 distinct; length 7-7 | values: `Suite 0` | constant in this data |
| `cc_city` | VARCHAR | 1 distinct; length 6-6 | values: `Midway` | constant in this data |
| `cc_county` | VARCHAR | 1 distinct; length 17-17 | values: `Williamson County` | constant in this data |
| `cc_state` | VARCHAR | 1 distinct; length 2-2 | values: `TN` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `cc_zip` | VARCHAR | 1 distinct; length 5-5 | values: `31904` | constant in this data |
| `cc_country` | VARCHAR | 1 distinct; length 13-13 | values: `United States` | constant in this data |
| `cc_gmt_offset` | DECIMAL(5,2) | 1 distinct; -5.00 to -5.00 | values: `-5.0` | constant in this data |
| `cc_tax_percentage` | DECIMAL(5,2) | 1 distinct; 0.11 to 0.11 | values: `0.11` | constant in this data |

## catalog_page (11,718 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `cp_catalog_page_sk` | BIGINT | 11,718 distinct; 1 to 11718 |  |  |
| `cp_catalog_page_id` | VARCHAR | 11,718 distinct; length 16-16 | e.g. `AAAAAAAAAAABAAAA`, `AAAAAAAAAAACAAAA`, `AAAAAAAAAABAAAAA` |  |
| `cp_start_date_sk` | BIGINT | 91 distinct; 101 nulls; 2450815 to 2453005 |  |  |
| `cp_end_date_sk` | BIGINT | 97 distinct; 108 nulls; 2450844 to 2453186 |  |  |
| `cp_department` | VARCHAR | 1 distinct; 120 nulls; length 10-10 | values: `DEPARTMENT` | constant in this data |
| `cp_catalog_number` | BIGINT | 109 distinct; 104 nulls; 1 to 109 |  |  |
| `cp_catalog_page_number` | BIGINT | 108 distinct; 116 nulls; 1 to 108 |  |  |
| `cp_description` | VARCHAR | 11,609 distinct; 109 nulls; length 50-99 | e.g. `A bit asleep rooms cannot feel short dry secondary leads. Ab`, `A bit black rocks ought to happen level, wise tools. Shows shall know modern pupils. Actually new`, `A bit immense forms must not hear afterwards for example powerful men. Parliamen` |  |
| `cp_type` | VARCHAR | 3 distinct; 110 nulls; length 7-9 | values: `bi-annual`, `monthly`, `quarterly` |  |

## catalog_returns (1,377 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `cr_returned_date_sk` | BIGINT | 890 distinct; 2450878 to 2452490 |  |  |
| `cr_returned_time_sk` | BIGINT | 1,363 distinct; 263 to 86370 |  |  |
| `cr_item_sk` | BIGINT | 150 distinct; 1 to 179 |  |  |
| `cr_refunded_customer_sk` | BIGINT | 593 distinct; 29 nulls; 3 to 1000 |  |  |
| `cr_refunded_cdemo_sk` | BIGINT | 894 distinct; 30 nulls; 9 to 19179 |  |  |
| `cr_refunded_hdemo_sk` | BIGINT | 866 distinct; 24 nulls; 2 to 7193 |  |  |
| `cr_refunded_addr_sk` | BIGINT | 411 distinct; 27 nulls; 1 to 500 |  |  |
| `cr_returning_customer_sk` | BIGINT | 733 distinct; 29 nulls; 2 to 1000 |  |  |
| `cr_returning_cdemo_sk` | BIGINT | 1,293 distinct; 33 nulls; 9 to 19191 |  |  |
| `cr_returning_hdemo_sk` | BIGINT | 1,216 distinct; 35 nulls; 7 to 7199 |  |  |
| `cr_returning_addr_sk` | BIGINT | 465 distinct; 32 nulls; 1 to 500 |  |  |
| `cr_call_center_sk` | BIGINT | 1 distinct; 29 nulls; 1 to 1 | values: `1` | constant in this data |
| `cr_catalog_page_sk` | BIGINT | 1,004 distinct; 31 nulls; 2 to 6919 |  |  |
| `cr_ship_mode_sk` | BIGINT | 20 distinct; 33 nulls; 1 to 20 |  |  |
| `cr_warehouse_sk` | BIGINT | 1 distinct; 25 nulls; 1 to 1 | values: `1` | constant in this data |
| `cr_reason_sk` | BIGINT | 1 distinct; 32 nulls; 1 to 1 | values: `1` | constant in this data |
| `cr_order_number` | BIGINT | 928 distinct; 2 to 1600 |  |  |
| `cr_return_quantity` | BIGINT | 93 distinct; 27 nulls; 1 to 96 |  |  |
| `cr_return_amount` | DECIMAL(7,2) | 1,316 distinct; 37 nulls; 0.00 to 15,059.70 |  |  |
| `cr_return_tax` | DECIMAL(7,2) | 1,069 distinct; 31 nulls; 0.00 to 1,054.17 |  |  |
| `cr_return_amt_inc_tax` | DECIMAL(7,2) | 1,327 distinct; 33 nulls; 0.00 to 16,113.87 |  |  |
| `cr_fee` | DECIMAL(7,2) | 1,262 distinct; 32 nulls; 0.54 to 99.99 |  |  |
| `cr_return_ship_cost` | DECIMAL(7,2) | 1,298 distinct; 28 nulls; 0.00 to 8,444.16 |  |  |
| `cr_refunded_cash` | DECIMAL(7,2) | 1,310 distinct; 27 nulls; 0.00 to 13,661.36 |  |  |
| `cr_reversed_charge` | DECIMAL(7,2) | 1,271 distinct; 30 nulls; 0.00 to 6,893.02 |  |  |
| `cr_store_credit` | DECIMAL(7,2) | 1,261 distinct; 28 nulls; 0.00 to 5,662.80 |  |  |
| `cr_net_loss` | DECIMAL(7,2) | 1,340 distinct; 32 nulls; 3.87 to 8,666.46 |  |  |

## catalog_sales (14,313 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `cs_sold_date_sk` | BIGINT | 1,408 distinct; 80 nulls; 2450815 to 2452225 |  |  |
| `cs_sold_time_sk` | BIGINT | 1,582 distinct; 86 nulls; 133 to 86298 |  |  |
| `cs_ship_date_sk` | BIGINT | 1,486 distinct; 88 nulls; 2450820 to 2452313 |  |  |
| `cs_bill_customer_sk` | BIGINT | 791 distinct; 81 nulls; 3 to 1000 |  |  |
| `cs_bill_cdemo_sk` | BIGINT | 1,542 distinct; 73 nulls; 9 to 19197 |  |  |
| `cs_bill_hdemo_sk` | BIGINT | 1,435 distinct; 70 nulls; 2 to 7200 |  |  |
| `cs_bill_addr_sk` | BIGINT | 480 distinct; 79 nulls; 1 to 500 |  |  |
| `cs_ship_customer_sk` | BIGINT | 795 distinct; 84 nulls; 3 to 1000 |  |  |
| `cs_ship_cdemo_sk` | BIGINT | 1,534 distinct; 81 nulls; 9 to 19201 |  |  |
| `cs_ship_hdemo_sk` | BIGINT | 1,430 distinct; 83 nulls; 2 to 7200 |  |  |
| `cs_ship_addr_sk` | BIGINT | 478 distinct; 102 nulls; 1 to 500 |  |  |
| `cs_call_center_sk` | BIGINT | 1 distinct; 63 nulls; 1 to 1 | values: `1` | constant in this data |
| `cs_catalog_page_sk` | BIGINT | 3,426 distinct; 70 nulls; 1 to 7020 |  |  |
| `cs_ship_mode_sk` | BIGINT | 20 distinct; 83 nulls; 1 to 20 |  |  |
| `cs_warehouse_sk` | BIGINT | 1 distinct; 83 nulls; 1 to 1 | values: `1` | constant in this data |
| `cs_item_sk` | BIGINT | 150 distinct; 1 to 179 |  |  |
| `cs_promo_sk` | BIGINT | 3 distinct; 69 nulls; 1 to 3 | values: `1`, `2`, `3` |  |
| `cs_order_number` | BIGINT | 1,600 distinct; 1 to 1600 |  |  |
| `cs_quantity` | BIGINT | 100 distinct; 68 nulls; 1 to 100 |  |  |
| `cs_wholesale_cost` | DECIMAL(7,2) | 7,547 distinct; 70 nulls; 1.02 to 100.00 |  |  |
| `cs_list_price` | DECIMAL(7,2) | 10,503 distinct; 85 nulls; 1.14 to 297.39 |  |  |
| `cs_sales_price` | DECIMAL(7,2) | 8,263 distinct; 85 nulls; 0.00 to 274.47 |  |  |
| `cs_ext_discount_amt` | DECIMAL(7,2) | 13,370 distinct; 76 nulls; 0.00 to 24,991.20 |  |  |
| `cs_ext_sales_price` | DECIMAL(7,2) | 13,395 distinct; 83 nulls; 0.00 to 22,732.08 |  |  |
| `cs_ext_wholesale_cost` | DECIMAL(7,2) | 13,687 distinct; 72 nulls; 1.49 to 9,892.08 |  |  |
| `cs_ext_list_price` | DECIMAL(7,2) | 13,957 distinct; 88 nulls; 1.66 to 27,457.00 |  |  |
| `cs_ext_tax` | DECIMAL(7,2) | 8,713 distinct; 77 nulls; 0.00 to 2,043.20 |  |  |
| `cs_coupon_amt` | DECIMAL(7,2) | 2,825 distinct; 70 nulls; 0.00 to 17,947.34 |  |  |
| `cs_ext_ship_cost` | DECIMAL(7,2) | 12,718 distinct; 72 nulls; 0.00 to 12,452.00 |  |  |
| `cs_net_paid` | DECIMAL(7,2) | 13,437 distinct; 89 nulls; 0.00 to 22,732.08 |  |  |
| `cs_net_paid_inc_tax` | DECIMAL(7,2) | 13,704 distinct; 94 nulls; 0.00 to 24,745.44 |  |  |
| `cs_net_paid_inc_ship` | DECIMAL(7,2) | 13,924 distinct; 0.00 to 33,107.36 |  |  |
| `cs_net_paid_inc_ship_tax` | DECIMAL(7,2) | 14,146 distinct; 0.00 to 35,150.56 |  |  |
| `cs_net_profit` | DECIMAL(7,2) | 13,772 distinct; -9,628.50 to 14,575.44 |  |  |

## customer (1,000 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `c_customer_sk` | BIGINT | 1,000 distinct; 1 to 1000 |  |  |
| `c_customer_id` | VARCHAR | 1,000 distinct; length 16-16 | e.g. `AAAAAAAAAABAAAAA`, `AAAAAAAAAACAAAAA`, `AAAAAAAAAADAAAAA` |  |
| `c_current_cdemo_sk` | BIGINT | 949 distinct; 26 nulls; 24 to 19179 |  |  |
| `c_current_hdemo_sk` | BIGINT | 904 distinct; 28 nulls; 1 to 7193 |  |  |
| `c_current_addr_sk` | BIGINT | 431 distinct; 1 to 500 |  |  |
| `c_first_shipto_date_sk` | BIGINT | 858 distinct; 35 nulls; 2449032 to 2452672 |  |  |
| `c_first_sales_date_sk` | BIGINT | 858 distinct; 30 nulls; 2449002 to 2452642 |  |  |
| `c_salutation` | VARCHAR | 6 distinct; 30 nulls; length 3-4 | values: `Dr.`, `Miss`, `Mr.`, `Mrs.`, `Ms.`, `Sir` |  |
| `c_first_name` | VARCHAR | 517 distinct; 32 nulls; length 2-11 | e.g. `Aaron`, `Adam`, `Adela` |  |
| `c_last_name` | VARCHAR | 667 distinct; 24 nulls; length 3-13 | e.g. `Adams`, `Aguilar`, `Ahrens` |  |
| `c_preferred_cust_flag` | VARCHAR | 2 distinct; 29 nulls; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `c_birth_day` | BIGINT | 31 distinct; 38 nulls; 1 to 31 |  |  |
| `c_birth_month` | BIGINT | 12 distinct; 34 nulls; 1 to 12 |  |  |
| `c_birth_year` | BIGINT | 69 distinct; 31 nulls; 1924 to 1992 |  |  |
| `c_birth_country` | VARCHAR | 210 distinct; 31 nulls; length 4-20 | e.g. `AFGHANISTAN`, `ALAND ISLANDS`, `ALBANIA` |  |
| `c_login` | VARCHAR | 0 distinct; 1,000 nulls | values:  |  |
| `c_email_address` | VARCHAR | 969 distinct; 31 nulls; length 15-41 | e.g. `Aaron.Browder@iUpddkHI9z8.org`, `Aaron.Fuller@Y4M99U.com`, `Aaron.Labbe@0znR.com` |  |
| `c_last_review_date_sk` | INTEGER | 343 distinct; 25 nulls; 2452283 to 2452648 |  |  |

## customer_address (500 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ca_address_sk` | BIGINT | 500 distinct; 1 to 500 |  |  |
| `ca_address_id` | VARCHAR | 500 distinct; length 16-16 | e.g. `AAAAAAAAAABAAAAA`, `AAAAAAAAABAAAAAA`, `AAAAAAAAABBAAAAA` |  |
| `ca_street_number` | VARCHAR | 399 distinct; 14 nulls; length 1-3 | e.g. `10`, `102`, `103` |  |
| `ca_street_name` | VARCHAR | 305 distinct; 16 nulls; length 4-18 | e.g. `10th `, `10th 10th`, `10th Oak` |  |
| `ca_street_type` | VARCHAR | 20 distinct; 17 nulls; length 2-9 | values: `Ave`, `Avenue`, `Blvd`, `Boulevard`, `Cir.`, `Circle`, `Court`, `Ct.`, `Dr.`, `Drive`, `Lane`, `Ln`, `Parkway`, `Pkwy`, `RD`, `Road`, `ST`, `Street`, `Way`, `Wy` |  |
| `ca_suite_number` | VARCHAR | 75 distinct; 15 nulls; length 7-9 | e.g. `Suite 0`, `Suite 10`, `Suite 100` |  |
| `ca_city` | VARCHAR | 151 distinct; 14 nulls; length 4-16 | e.g. `Allentown`, `Altamont`, `Antioch` |  |
| `ca_county` | VARCHAR | 373 distinct; 14 nulls; length 10-28 | e.g. `Ada County`, `Adair County`, `Albany County` |  |
| `ca_state` | VARCHAR | 49 distinct; 12 nulls; length 2-2 | e.g. `AK`, `AL`, `AR` |  |
| `ca_zip` | VARCHAR | 388 distinct; 16 nulls; length 5-5 | e.g. `00791`, `00969`, `00999` |  |
| `ca_country` | VARCHAR | 1 distinct; 16 nulls; length 13-13 | values: `United States` | constant in this data |
| `ca_gmt_offset` | DECIMAL(5,2) | 6 distinct; 13 nulls; -10.00 to -5.00 | values: `-10.0`, `-9.0`, `-8.0`, `-7.0`, `-6.0`, `-5.0` |  |
| `ca_location_type` | VARCHAR | 3 distinct; 15 nulls; length 5-13 | values: `apartment`, `condo`, `single family` |  |

## customer_demographics (19,208 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `cd_demo_sk` | BIGINT | 19,208 distinct; 1 to 19208 |  |  |
| `cd_gender` | VARCHAR | 2 distinct; length 1-1 | values: `F`, `M` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `cd_marital_status` | VARCHAR | 5 distinct; length 1-1 | values: `D`, `M`, `S`, `U`, `W` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `cd_education_status` | VARCHAR | 7 distinct; length 7-15 | values: `2 yr Degree`, `4 yr Degree`, `Advanced Degree`, `College`, `Primary`, `Secondary`, `Unknown` |  |
| `cd_purchase_estimate` | BIGINT | 20 distinct; 500 to 10000 |  |  |
| `cd_credit_rating` | VARCHAR | 4 distinct; length 4-9 | values: `Good`, `High Risk`, `Low Risk`, `Unknown` |  |
| `cd_dep_count` | BIGINT | 4 distinct; 0 to 3 | values: `0`, `1`, `2`, `3` |  |
| `cd_dep_employed_count` | BIGINT | 1 distinct; 0 to 0 | values: `0` | constant in this data |
| `cd_dep_college_count` | INTEGER | 1 distinct; 0 to 0 | values: `0` | constant in this data |

## date_dim (73,049 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `d_date_sk` | BIGINT | 73,049 distinct; 2415022 to 2488070 |  |  |
| `d_date_id` | VARCHAR | 73,049 distinct; length 16-16 | e.g. `AAAAAAAAAAAAFCAA`, `AAAAAAAAAAABFCAA`, `AAAAAAAAAAACFCAA` |  |
| `d_date` | DATE | 73,049 distinct; 1900-01-02 to 2100-01-01 |  |  |
| `d_month_seq` | BIGINT | 2,401 distinct; 0 to 2400 |  |  |
| `d_week_seq` | BIGINT | 10,436 distinct; 1 to 10436 |  |  |
| `d_quarter_seq` | BIGINT | 801 distinct; 1 to 801 |  |  |
| `d_year` | BIGINT | 201 distinct; 1900 to 2100 |  |  |
| `d_dow` | BIGINT | 7 distinct; 0 to 6 | values: `0`, `1`, `2`, `3`, `4`, `5`, `6` |  |
| `d_moy` | BIGINT | 12 distinct; 1 to 12 |  |  |
| `d_dom` | BIGINT | 31 distinct; 1 to 31 |  |  |
| `d_qoy` | BIGINT | 4 distinct; 1 to 4 | values: `1`, `2`, `3`, `4` |  |
| `d_fy_year` | BIGINT | 201 distinct; 1900 to 2100 |  |  |
| `d_fy_quarter_seq` | BIGINT | 801 distinct; 1 to 801 |  |  |
| `d_fy_week_seq` | BIGINT | 10,436 distinct; 1 to 10436 |  |  |
| `d_day_name` | VARCHAR | 7 distinct; length 6-9 | values: `Friday`, `Monday`, `Saturday`, `Sunday`, `Thursday`, `Tuesday`, `Wednesday` |  |
| `d_quarter_name` | VARCHAR | 801 distinct; length 6-6 | e.g. `1900Q1`, `1900Q2`, `1900Q3` |  |
| `d_holiday` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_weekend` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_following_holiday` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_first_dom` | BIGINT | 2,401 distinct; 2415021 to 2488070 |  |  |
| `d_last_dom` | BIGINT | 2,401 distinct; 2415020 to 2488372 |  |  |
| `d_same_day_ly` | BIGINT | 73,000 distinct; 2414657 to 2487705 |  |  |
| `d_same_day_lq` | BIGINT | 72,698 distinct; 2414930 to 2487978 |  |  |
| `d_current_day` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_current_week` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_current_month` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_current_quarter` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `d_current_year` | VARCHAR | 2 distinct; length 1-1 | values: `N`, `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |

## household_demographics (7,200 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `hd_demo_sk` | BIGINT | 7,200 distinct; 1 to 7200 |  |  |
| `hd_income_band_sk` | BIGINT | 20 distinct; 1 to 20 |  |  |
| `hd_buy_potential` | VARCHAR | 6 distinct; length 5-10 | values: `0-500`, `1001-5000`, `5001-10000`, `501-1000`, `>10000`, `Unknown` |  |
| `hd_dep_count` | BIGINT | 10 distinct; 0 to 9 | values: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9` |  |
| `hd_vehicle_count` | INTEGER | 6 distinct; -1 to 4 | values: `-1`, `0`, `1`, `2`, `3`, `4` |  |

## income_band (20 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ib_income_band_sk` | BIGINT | 20 distinct; 1 to 20 |  |  |
| `ib_lower_bound` | BIGINT | 20 distinct; 0 to 190001 |  |  |
| `ib_upper_bound` | INTEGER | 20 distinct; 10000 to 200000 |  |  |

## inventory (23,490 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `inv_date_sk` | BIGINT | 261 distinct; 2450815 to 2452635 |  |  |
| `inv_item_sk` | BIGINT | 180 distinct; 1 to 180 |  |  |
| `inv_warehouse_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `inv_quantity_on_hand` | INTEGER | 1,001 distinct; 1,162 nulls; 0 to 1000 |  |  |

## item (180 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `i_item_sk` | BIGINT | 180 distinct; 1 to 180 |  |  |
| `i_item_id` | VARCHAR | 90 distinct; length 16-16 | e.g. `AAAAAAAAABAAAAAA`, `AAAAAAAAACAAAAAA`, `AAAAAAAAAEAAAAAA` |  |
| `i_rec_start_date` | DATE | 4 distinct; 1997-10-27 to 2001-10-27 | values: `1997-10-27`, `1999-10-28`, `2000-10-27`, `2001-10-27` |  |
| `i_rec_end_date` | DATE | 3 distinct; 90 nulls; 1999-10-27 to 2001-10-26 | values: `1999-10-27`, `2000-10-26`, `2001-10-26` |  |
| `i_item_desc` | VARCHAR | 136 distinct; length 1-198 | e.g. `A little special changes would not turn certainly terms. Big, immediate earn`, `Activities cover `, `Again common customers should make hardly proposals. Close groups can prevent after a cars. Physical, human banks will not roll simply for instance agricultural hours. Northern centre` |  |
| `i_current_price` | DECIMAL(7,2) | 169 distinct; 0.11 to 98.66 |  |  |
| `i_wholesale_cost` | DECIMAL(7,2) | 124 distinct; 0.06 to 85.83 |  |  |
| `i_brand_id` | BIGINT | 86 distinct; 1001001 to 10016012 |  |  |
| `i_brand` | VARCHAR | 111 distinct; length 11-21 | e.g. `amalgamalg #1`, `amalgamalgamalg #5`, `amalgamalgamalg #6` |  |
| `i_class_id` | BIGINT | 16 distinct; 1 to 16 |  |  |
| `i_class` | VARCHAR | 71 distinct; length 3-15 | e.g. `accessories`, `arts`, `athletic` |  |
| `i_category_id` | BIGINT | 10 distinct; 1 to 10 | values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10` |  |
| `i_category` | VARCHAR | 10 distinct; length 3-11 | values: `Books`, `Children`, `Electronics`, `Home`, `Jewelry`, `Men`, `Music`, `Shoes`, `Sports`, `Women` |  |
| `i_manufact_id` | BIGINT | 130 distinct; 2 to 995 |  |  |
| `i_manufact` | VARCHAR | 106 distinct; length 7-15 | e.g. `ableablecally`, `ableablepri`, `ableanti` |  |
| `i_size` | VARCHAR | 7 distinct; length 3-11 | values: `N/A`, `economy`, `extra large`, `large`, `medium`, `petite`, `small` |  |
| `i_formulation` | VARCHAR | 140 distinct; length 20-20 | e.g. `01329slate7866063154`, `01882924064yellow241`, `027315130steel656106` |  |
| `i_color` | VARCHAR | 62 distinct; length 3-9 | e.g. `bisque`, `black`, `blue` |  |
| `i_units` | VARCHAR | 21 distinct; length 2-7 | values: `Box`, `Bunch`, `Bundle`, `Carton`, `Case`, `Cup`, `Dozen`, `Dram`, `Each`, `Gram`, `Gross`, `Lb`, `N/A`, `Ounce`, `Oz`, `Pallet`, `Pound`, `Tbl`, `Ton`, `Tsp`, `Unknown` |  |
| `i_container` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `i_manager_id` | BIGINT | 70 distinct; 1 to 98 |  |  |
| `i_product_name` | VARCHAR | 180 distinct; length 3-15 | e.g. `able`, `ableable`, `ableableought` |  |

## promotion (3 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `p_promo_sk` | BIGINT | 3 distinct; 1 to 3 | values: `1`, `2`, `3` |  |
| `p_promo_id` | VARCHAR | 3 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA`, `AAAAAAAACAAAAAAA`, `AAAAAAAADAAAAAAA` |  |
| `p_start_date_sk` | BIGINT | 3 distinct; 2450118 to 2450675 | values: `2450118`, `2450164`, `2450675` |  |
| `p_end_date_sk` | BIGINT | 3 distinct; 2450150 to 2450712 | values: `2450150`, `2450185`, `2450712` |  |
| `p_item_sk` | BIGINT | 3 distinct; 43 to 122 | values: `43`, `70`, `122` |  |
| `p_cost` | DECIMAL(15,2) | 1 distinct; 1,000.00 to 1,000.00 | values: `1000.0` | constant in this data |
| `p_response_target` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `p_promo_name` | VARCHAR | 3 distinct; length 3-5 | values: `able`, `ought`, `pri` |  |
| `p_channel_dmail` | VARCHAR | 1 distinct; length 1-1 | values: `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_email` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_catalog` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_tv` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_radio` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_press` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_event` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_demo` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `p_channel_details` | VARCHAR | 3 distinct; length 22-40 | values: `Companies shall not pr`, `Men will not say merely. Old, available `, `So willing buildings coul` |  |
| `p_purpose` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `p_discount_active` | VARCHAR | 1 distinct; length 1-1 | values: `N` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |

## reason (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `r_reason_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `r_reason_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `r_reason_desc` | VARCHAR | 1 distinct; length 19-19 | values: `Package was damaged` | constant in this data |

## ship_mode (20 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `sm_ship_mode_sk` | BIGINT | 20 distinct; 1 to 20 |  |  |
| `sm_ship_mode_id` | VARCHAR | 20 distinct; length 16-16 | values: `AAAAAAAAABAAAAAA`, `AAAAAAAABAAAAAAA`, `AAAAAAAABBAAAAAA`, `AAAAAAAACAAAAAAA`, `AAAAAAAACBAAAAAA`, `AAAAAAAADAAAAAAA`, `AAAAAAAADBAAAAAA`, `AAAAAAAAEAAAAAAA`, `AAAAAAAAEBAAAAAA`, `AAAAAAAAFAAAAAAA`, `AAAAAAAAGAAAAAAA`, `AAAAAAAAHAAAAAAA`, `AAAAAAAAIAAAAAAA`, `AAAAAAAAJAAAAAAA`, `AAAAAAAAKAAAAAAA`, `AAAAAAAALAAAAAAA`, `AAAAAAAAMAAAAAAA`, `AAAAAAAANAAAAAAA`, `AAAAAAAAOAAAAAAA`, `AAAAAAAAPAAAAAAA` |  |
| `sm_type` | VARCHAR | 6 distinct; length 7-9 | values: `EXPRESS`, `LIBRARY`, `NEXT DAY`, `OVERNIGHT`, `REGULAR`, `TWO DAY` |  |
| `sm_code` | VARCHAR | 4 distinct; length 3-7 | values: `AIR`, `BIKE`, `SEA`, `SURFACE` |  |
| `sm_carrier` | VARCHAR | 20 distinct; length 3-14 | values: `AIRBORNE`, `ALLIANCE`, `BARIAN`, `BOXBUNDLES`, `DHL`, `DIAMOND`, `FEDEX`, `GERMA`, `GREAT EASTERN`, `HARMSTORF`, `LATVIAN`, `MSC`, `ORIENTAL`, `PRIVATECARRIER`, `RUPEKSA`, `TBS`, `UPS`, `USPS`, `ZHOU`, `ZOUROS` |  |
| `sm_contract` | VARCHAR | 20 distinct; length 2-20 | values: `2mM8l`, `5FKNB0j8aaqTB`, `6Hzzp4JkzjqD8MGXLCDa`, `A5BYO1qH8HGTTN`, `Ek`, `GNJr3g5i7oorKqtX`, `HVDFCcQ`, `I3uCelXtjP`, `O9V6oF8RJnLMmZYd1`, `OrDuVy2H`, `P7FBIt8yd`, `UaAJjKDnL4gTOqbpj`, `Xjy3ZPuiDjzHlRx14Z3`, `YvxVaJI10`, `fop0bcSd91J26IVpR`, `hGoF18SLDDPBj`, `ldhM8IvpzHgdbBgDfI`, `qENFQ`, `uukTktPYycct8`, `yVfotg7Tio3MVhBg6Bkn` |  |

## store (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `s_store_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `s_store_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `s_rec_start_date` | DATE | 1 distinct; 1997-03-13 to 1997-03-13 | values: `1997-03-13` | constant in this data |
| `s_rec_end_date` | DATE | 0 distinct; 1 nulls; None to None | values:  |  |
| `s_closed_date_sk` | BIGINT | 1 distinct; 2451189 to 2451189 | values: `2451189` | constant in this data |
| `s_store_name` | VARCHAR | 1 distinct; length 5-5 | values: `ought` | constant in this data |
| `s_number_employees` | BIGINT | 1 distinct; 245 to 245 | values: `245` | constant in this data |
| `s_floor_space` | BIGINT | 1 distinct; 5250760 to 5250760 | values: `5250760` | constant in this data |
| `s_hours` | VARCHAR | 1 distinct; length 7-7 | values: `8AM-4PM` | constant in this data |
| `s_manager` | VARCHAR | 1 distinct; length 12-12 | values: `William Ward` | constant in this data |
| `s_market_id` | BIGINT | 1 distinct; 2 to 2 | values: `2` | constant in this data |
| `s_geography_class` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `s_market_desc` | VARCHAR | 1 distinct; length 56-56 | values: `Enough high areas stop expectations. Elaborate, local is` | constant in this data |
| `s_market_manager` | VARCHAR | 1 distinct; length 15-15 | values: `Charles Bartley` | constant in this data |
| `s_division_id` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `s_division_name` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `s_company_id` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `s_company_name` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `s_street_number` | VARCHAR | 1 distinct; length 3-3 | values: `767` | constant in this data |
| `s_street_name` | VARCHAR | 1 distinct; length 7-7 | values: `Spring ` | constant in this data |
| `s_street_type` | VARCHAR | 1 distinct; length 2-2 | values: `Wy` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `s_suite_number` | VARCHAR | 1 distinct; length 9-9 | values: `Suite 250` | constant in this data |
| `s_city` | VARCHAR | 1 distinct; length 6-6 | values: `Midway` | constant in this data |
| `s_county` | VARCHAR | 1 distinct; length 17-17 | values: `Williamson County` | constant in this data |
| `s_state` | VARCHAR | 1 distinct; length 2-2 | values: `TN` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `s_zip` | VARCHAR | 1 distinct; length 5-5 | values: `31904` | constant in this data |
| `s_country` | VARCHAR | 1 distinct; length 13-13 | values: `United States` | constant in this data |
| `s_gmt_offset` | DECIMAL(5,2) | 1 distinct; -5.00 to -5.00 | values: `-5.0` | constant in this data |
| `s_tax_percentage` | DECIMAL(5,2) | 1 distinct; 0.03 to 0.03 | values: `0.03` | constant in this data |

## store_returns (2,829 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `sr_returned_date_sk` | BIGINT | 1,413 distinct; 109 nulls; 2450839 to 2452814 |  |  |
| `sr_return_time_sk` | BIGINT | 2,602 distinct; 97 nulls; 28799 to 61187 |  |  |
| `sr_item_sk` | BIGINT | 180 distinct; 1 to 180 |  |  |
| `sr_customer_sk` | BIGINT | 861 distinct; 100 nulls; 2 to 1000 |  |  |
| `sr_cdemo_sk` | BIGINT | 2,533 distinct; 104 nulls; 6 to 19206 |  |  |
| `sr_hdemo_sk` | BIGINT | 2,291 distinct; 101 nulls; 4 to 7192 |  |  |
| `sr_addr_sk` | BIGINT | 500 distinct; 110 nulls; 1 to 500 |  |  |
| `sr_store_sk` | BIGINT | 1 distinct; 107 nulls; 1 to 1 | values: `1` | constant in this data |
| `sr_reason_sk` | BIGINT | 1 distinct; 95 nulls; 1 to 1 | values: `1` | constant in this data |
| `sr_ticket_number` | BIGINT | 1,699 distinct; 1 to 2400 |  |  |
| `sr_return_quantity` | BIGINT | 96 distinct; 113 nulls; 1 to 96 |  |  |
| `sr_return_amt` | DECIMAL(7,2) | 2,604 distinct; 110 nulls; 0.00 to 11,614.59 |  |  |
| `sr_return_tax` | DECIMAL(7,2) | 1,907 distinct; 106 nulls; 0.00 to 728.37 |  |  |
| `sr_return_amt_inc_tax` | DECIMAL(7,2) | 2,652 distinct; 100 nulls; 0.00 to 11,846.88 |  |  |
| `sr_fee` | DECIMAL(7,2) | 2,357 distinct; 102 nulls; 0.51 to 100.00 |  |  |
| `sr_return_ship_cost` | DECIMAL(7,2) | 2,548 distinct; 115 nulls; 0.00 to 6,604.68 |  |  |
| `sr_refunded_cash` | DECIMAL(7,2) | 2,567 distinct; 105 nulls; 0.00 to 7,799.68 |  |  |
| `sr_reversed_charge` | DECIMAL(7,2) | 2,395 distinct; 112 nulls; 0.00 to 5,656.42 |  |  |
| `sr_store_credit` | DECIMAL(7,2) | 2,357 distinct; 103 nulls; 0.00 to 7,386.71 |  |  |
| `sr_net_loss` | DECIMAL(7,2) | 2,674 distinct; 104 nulls; 1.70 to 6,824.59 |  |  |

## store_sales (28,810 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ss_sold_date_sk` | BIGINT | 1,200 distinct; 1,202 nulls; 2450816 to 2452642 |  |  |
| `ss_sold_time_sk` | BIGINT | 2,336 distinct; 1,228 nulls; 28873 to 75573 |  |  |
| `ss_item_sk` | BIGINT | 180 distinct; 1 to 180 |  |  |
| `ss_customer_sk` | BIGINT | 914 distinct; 1,224 nulls; 1 to 1000 |  |  |
| `ss_cdemo_sk` | BIGINT | 2,257 distinct; 1,242 nulls; 12 to 19208 |  |  |
| `ss_hdemo_sk` | BIGINT | 2,039 distinct; 1,277 nulls; 5 to 7200 |  |  |
| `ss_addr_sk` | BIGINT | 499 distinct; 1,229 nulls; 1 to 500 |  |  |
| `ss_store_sk` | BIGINT | 1 distinct; 1,256 nulls; 1 to 1 | values: `1` | constant in this data |
| `ss_promo_sk` | BIGINT | 3 distinct; 1,226 nulls; 1 to 3 | values: `1`, `2`, `3` |  |
| `ss_ticket_number` | BIGINT | 2,400 distinct; 1 to 2400 |  |  |
| `ss_quantity` | BIGINT | 100 distinct; 1,284 nulls; 1 to 100 |  |  |
| `ss_wholesale_cost` | DECIMAL(7,2) | 9,298 distinct; 1,229 nulls; 1.00 to 100.00 |  |  |
| `ss_list_price` | DECIMAL(7,2) | 13,498 distinct; 1,254 nulls; 1.03 to 199.72 |  |  |
| `ss_sales_price` | DECIMAL(7,2) | 9,832 distinct; 1,245 nulls; 0.00 to 188.67 |  |  |
| `ss_ext_discount_amt` | DECIMAL(7,2) | 5,209 distinct; 1,194 nulls; 0.00 to 15,389.98 |  |  |
| `ss_ext_sales_price` | DECIMAL(7,2) | 24,314 distinct; 1,229 nulls; 0.00 to 17,255.70 |  |  |
| `ss_ext_wholesale_cost` | DECIMAL(7,2) | 25,652 distinct; 1,243 nulls; 1.16 to 9,993.00 |  |  |
| `ss_ext_list_price` | DECIMAL(7,2) | 26,253 distinct; 1,209 nulls; 1.29 to 18,888.52 |  |  |
| `ss_ext_tax` | DECIMAL(7,2) | 12,724 distinct; 1,228 nulls; 0.00 to 1,530.00 |  |  |
| `ss_coupon_amt` | DECIMAL(7,2) | 5,209 distinct; 1,194 nulls; 0.00 to 15,389.98 |  |  |
| `ss_net_paid` | DECIMAL(7,2) | 24,560 distinct; 1,242 nulls; 0.00 to 17,255.70 |  |  |
| `ss_net_paid_inc_tax` | DECIMAL(7,2) | 25,590 distinct; 1,259 nulls; 0.00 to 17,943.10 |  |  |
| `ss_net_profit` | DECIMAL(7,2) | 25,318 distinct; 1,261 nulls; -9,538.98 to 7,987.00 |  |  |

## time_dim (86,400 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `t_time_sk` | BIGINT | 86,400 distinct; 0 to 86399 |  |  |
| `t_time_id` | VARCHAR | 86,400 distinct; length 16-16 | e.g. `AAAAAAAAAAAABAAA`, `AAAAAAAAAAABAAAA`, `AAAAAAAAAAABBAAA` |  |
| `t_time` | BIGINT | 86,400 distinct; 0 to 86399 |  |  |
| `t_hour` | BIGINT | 24 distinct; 0 to 23 |  |  |
| `t_minute` | BIGINT | 60 distinct; 0 to 59 |  |  |
| `t_second` | BIGINT | 60 distinct; 0 to 59 |  |  |
| `t_am_pm` | VARCHAR | 2 distinct; length 2-2 | values: `AM`, `PM` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `t_shift` | VARCHAR | 3 distinct; length 5-6 | values: `first`, `second`, `third` |  |
| `t_sub_shift` | VARCHAR | 4 distinct; length 5-9 | values: `afternoon`, `evening`, `morning`, `night` |  |
| `t_meal_time` | VARCHAR | 3 distinct; 50,400 nulls; length 5-9 | values: `breakfast`, `dinner`, `lunch` |  |

## warehouse (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `w_warehouse_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `w_warehouse_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `w_warehouse_name` | VARCHAR | 1 distinct; length 19-19 | values: `Conventional childr` | constant in this data |
| `w_warehouse_sq_ft` | BIGINT | 1 distinct; 977787 to 977787 | values: `977787` | constant in this data |
| `w_street_number` | VARCHAR | 1 distinct; length 3-3 | values: `651` | constant in this data |
| `w_street_name` | VARCHAR | 1 distinct; length 4-4 | values: `6th ` | constant in this data |
| `w_street_type` | VARCHAR | 1 distinct; length 7-7 | values: `Parkway` | constant in this data |
| `w_suite_number` | VARCHAR | 1 distinct; length 9-9 | values: `Suite 470` | constant in this data |
| `w_city` | VARCHAR | 1 distinct; length 6-6 | values: `Midway` | constant in this data |
| `w_county` | VARCHAR | 1 distinct; length 17-17 | values: `Williamson County` | constant in this data |
| `w_state` | VARCHAR | 1 distinct; length 2-2 | values: `TN` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `w_zip` | VARCHAR | 1 distinct; length 5-5 | values: `31904` | constant in this data |
| `w_country` | VARCHAR | 1 distinct; length 13-13 | values: `United States` | constant in this data |
| `w_gmt_offset` | DECIMAL(5,2) | 1 distinct; -5.00 to -5.00 | values: `-5.0` | constant in this data |

## web_page (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `wp_web_page_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `wp_web_page_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `wp_rec_start_date` | DATE | 1 distinct; 1997-09-03 to 1997-09-03 | values: `1997-09-03` | constant in this data |
| `wp_rec_end_date` | DATE | 0 distinct; 1 nulls; None to None | values:  |  |
| `wp_creation_date_sk` | BIGINT | 1 distinct; 2450810 to 2450810 | values: `2450810` | constant in this data |
| `wp_access_date_sk` | BIGINT | 1 distinct; 2452620 to 2452620 | values: `2452620` | constant in this data |
| `wp_autogen_flag` | VARCHAR | 1 distinct; length 1-1 | values: `Y` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `wp_customer_sk` | BIGINT | 1 distinct; 539 to 539 | values: `539` | constant in this data |
| `wp_url` | VARCHAR | 1 distinct; length 18-18 | values: `http://www.foo.com` | constant in this data |
| `wp_type` | VARCHAR | 1 distinct; length 7-7 | values: `welcome` | constant in this data |
| `wp_char_count` | BIGINT | 1 distinct; 2531 to 2531 | values: `2531` | constant in this data |
| `wp_link_count` | BIGINT | 1 distinct; 8 to 8 | values: `8` | constant in this data |
| `wp_image_count` | BIGINT | 1 distinct; 3 to 3 | values: `3` | constant in this data |
| `wp_max_ad_count` | INTEGER | 1 distinct; 4 to 4 | values: `4` | constant in this data |

## web_returns (685 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `wr_returned_date_sk` | BIGINT | 551 distinct; 30 nulls; 2450911 to 2452965 |  |  |
| `wr_returned_time_sk` | BIGINT | 648 distinct; 31 nulls; 53 to 85139 |  |  |
| `wr_item_sk` | BIGINT | 167 distinct; 1 to 180 |  |  |
| `wr_refunded_customer_sk` | BIGINT | 482 distinct; 39 nulls; 5 to 1000 |  |  |
| `wr_refunded_cdemo_sk` | BIGINT | 646 distinct; 30 nulls; 7 to 19179 |  |  |
| `wr_refunded_hdemo_sk` | BIGINT | 620 distinct; 29 nulls; 8 to 7188 |  |  |
| `wr_refunded_addr_sk` | BIGINT | 356 distinct; 36 nulls; 2 to 500 |  |  |
| `wr_returning_customer_sk` | BIGINT | 488 distinct; 25 nulls; 5 to 1000 |  |  |
| `wr_returning_cdemo_sk` | BIGINT | 647 distinct; 27 nulls; 7 to 19179 |  |  |
| `wr_returning_hdemo_sk` | BIGINT | 613 distinct; 36 nulls; 8 to 7188 |  |  |
| `wr_returning_addr_sk` | BIGINT | 359 distinct; 33 nulls; 2 to 500 |  |  |
| `wr_web_page_sk` | BIGINT | 1 distinct; 33 nulls; 1 to 1 | values: `1` | constant in this data |
| `wr_reason_sk` | BIGINT | 1 distinct; 21 nulls; 1 to 1 | values: `1` | constant in this data |
| `wr_order_number` | BIGINT | 425 distinct; 1 to 600 |  |  |
| `wr_return_quantity` | BIGINT | 86 distinct; 32 nulls; 1 to 93 |  |  |
| `wr_return_amt` | DECIMAL(7,2) | 648 distinct; 28 nulls; 0.00 to 20,323.94 |  |  |
| `wr_return_tax` | DECIMAL(7,2) | 555 distinct; 29 nulls; 0.00 to 860.17 |  |  |
| `wr_return_amt_inc_tax` | DECIMAL(7,2) | 643 distinct; 32 nulls; 0.00 to 20,323.94 |  |  |
| `wr_fee` | DECIMAL(7,2) | 638 distinct; 28 nulls; 0.57 to 99.75 |  |  |
| `wr_return_ship_cost` | DECIMAL(7,2) | 635 distinct; 35 nulls; 0.00 to 8,129.03 |  |  |
| `wr_refunded_cash` | DECIMAL(7,2) | 631 distinct; 34 nulls; 0.00 to 17,275.34 |  |  |
| `wr_reversed_charge` | DECIMAL(7,2) | 622 distinct; 32 nulls; 0.00 to 6,174.26 |  |  |
| `wr_account_credit` | DECIMAL(7,2) | 624 distinct; 32 nulls; 0.00 to 8,698.28 |  |  |
| `wr_net_loss` | DECIMAL(7,2) | 652 distinct; 33 nulls; 11.52 to 8,707.16 |  |  |

## web_sales (7,212 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `ws_sold_date_sk` | BIGINT | 497 distinct; 2 nulls; 2450818 to 2452642 |  |  |
| `ws_sold_time_sk` | BIGINT | 598 distinct; 791 to 85015 |  |  |
| `ws_ship_date_sk` | BIGINT | 1,807 distinct; 2 nulls; 2450824 to 2452758 |  |  |
| `ws_item_sk` | BIGINT | 180 distinct; 1 to 180 |  |  |
| `ws_bill_customer_sk` | BIGINT | 461 distinct; 3 nulls; 1 to 999 |  |  |
| `ws_bill_cdemo_sk` | BIGINT | 593 distinct; 3 nulls; 23 to 19202 |  |  |
| `ws_bill_hdemo_sk` | BIGINT | 581 distinct; 3 nulls; 1 to 7163 |  |  |
| `ws_bill_addr_sk` | BIGINT | 331 distinct; 2 nulls; 2 to 500 |  |  |
| `ws_ship_customer_sk` | BIGINT | 439 distinct; 2 to 998 |  |  |
| `ws_ship_cdemo_sk` | BIGINT | 591 distinct; 2 nulls; 7 to 19207 |  |  |
| `ws_ship_hdemo_sk` | BIGINT | 580 distinct; 2 nulls; 32 to 7187 |  |  |
| `ws_ship_addr_sk` | BIGINT | 352 distinct; 2 nulls; 1 to 500 |  |  |
| `ws_web_page_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `ws_web_site_sk` | BIGINT | 1 distinct; 2 nulls; 1 to 1 | values: `1` | constant in this data |
| `ws_ship_mode_sk` | BIGINT | 20 distinct; 4 nulls; 1 to 20 |  |  |
| `ws_warehouse_sk` | BIGINT | 1 distinct; 3 nulls; 1 to 1 | values: `1` | constant in this data |
| `ws_promo_sk` | BIGINT | 3 distinct; 2 nulls; 1 to 3 | values: `1`, `2`, `3` |  |
| `ws_order_number` | BIGINT | 600 distinct; 1 to 600 |  |  |
| `ws_quantity` | BIGINT | 100 distinct; 3 nulls; 1 to 100 |  |  |
| `ws_wholesale_cost` | DECIMAL(7,2) | 5,074 distinct; 2 nulls; 1.00 to 100.00 |  |  |
| `ws_list_price` | DECIMAL(7,2) | 6,206 distinct; 3 nulls; 1.07 to 292.73 |  |  |
| `ws_sales_price` | DECIMAL(7,2) | 5,338 distinct; 1 nulls; 0.00 to 285.59 |  |  |
| `ws_ext_discount_amt` | DECIMAL(7,2) | 6,948 distinct; 4 nulls; 0.00 to 28,179.47 |  |  |
| `ws_ext_sales_price` | DECIMAL(7,2) | 6,956 distinct; 2 nulls; 0.00 to 25,512.00 |  |  |
| `ws_ext_wholesale_cost` | DECIMAL(7,2) | 7,061 distinct; 2 nulls; 2.76 to 9,867.00 |  |  |
| `ws_ext_list_price` | DECIMAL(7,2) | 7,123 distinct; 7.14 to 28,179.47 |  |  |
| `ws_ext_tax` | DECIMAL(7,2) | 5,132 distinct; 2 nulls; 0.00 to 1,910.07 |  |  |
| `ws_coupon_amt` | DECIMAL(7,2) | 1,384 distinct; 2 nulls; 0.00 to 20,673.10 |  |  |
| `ws_ext_ship_cost` | DECIMAL(7,2) | 6,749 distinct; 3 nulls; 0.00 to 12,530.43 |  |  |
| `ws_net_paid` | DECIMAL(7,2) | 6,969 distinct; 3 nulls; 0.00 to 25,100.36 |  |  |
| `ws_net_paid_inc_tax` | DECIMAL(7,2) | 7,046 distinct; 3 nulls; 0.00 to 26,857.38 |  |  |
| `ws_net_paid_inc_ship` | DECIMAL(7,2) | 7,116 distinct; 0.00 to 35,641.72 |  |  |
| `ws_net_paid_inc_ship_tax` | DECIMAL(7,2) | 7,176 distinct; 0.00 to 37,398.74 |  |  |
| `ws_net_profit` | DECIMAL(7,2) | 7,065 distinct; -9,650.53 to 16,199.36 |  |  |

## web_site (1 rows)

| column | type | stats | values / samples | notes |
|---|---|---|---|---|
| `web_site_sk` | BIGINT | 1 distinct; 1 to 1 | values: `1` | constant in this data |
| `web_site_id` | VARCHAR | 1 distinct; length 16-16 | values: `AAAAAAAABAAAAAAA` | constant in this data |
| `web_rec_start_date` | DATE | 1 distinct; 1997-08-16 to 1997-08-16 | values: `1997-08-16` | constant in this data |
| `web_rec_end_date` | DATE | 0 distinct; 1 nulls; None to None | values:  |  |
| `web_name` | VARCHAR | 1 distinct; length 6-6 | values: `site_0` | constant in this data |
| `web_open_date_sk` | BIGINT | 1 distinct; 2450807 to 2450807 | values: `2450807` | constant in this data |
| `web_close_date_sk` | BIGINT | 0 distinct; 1 nulls; None to None | values:  |  |
| `web_class` | VARCHAR | 1 distinct; length 7-7 | values: `Unknown` | constant in this data |
| `web_manager` | VARCHAR | 1 distinct; length 14-14 | values: `Ronald Shaffer` | constant in this data |
| `web_mkt_id` | BIGINT | 1 distinct; 4 to 4 | values: `4` | constant in this data |
| `web_mkt_class` | VARCHAR | 1 distinct; length 46-46 | values: `Grey lines ought to result indeed centres. Tod` | constant in this data |
| `web_mkt_desc` | VARCHAR | 1 distinct; length 75-75 | values: `Well similar decisions used to keep hardly democratic, personal priorities.` | constant in this data |
| `web_market_manager` | VARCHAR | 1 distinct; length 10-10 | values: `Joe George` | constant in this data |
| `web_company_id` | BIGINT | 1 distinct; 6 to 6 | values: `6` | constant in this data |
| `web_company_name` | VARCHAR | 1 distinct; length 5-5 | values: `cally` | constant in this data |
| `web_street_number` | VARCHAR | 1 distinct; length 2-2 | values: `51` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `web_street_name` | VARCHAR | 1 distinct; length 14-14 | values: `Dogwood Sunset` | constant in this data |
| `web_street_type` | VARCHAR | 1 distinct; length 2-2 | values: `Ln` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `web_suite_number` | VARCHAR | 1 distinct; length 9-9 | values: `Suite 330` | constant in this data |
| `web_city` | VARCHAR | 1 distinct; length 6-6 | values: `Midway` | constant in this data |
| `web_county` | VARCHAR | 1 distinct; length 17-17 | values: `Williamson County` | constant in this data |
| `web_state` | VARCHAR | 1 distinct; length 2-2 | values: `TN` | coded: meaning needs docs (NO DOCS SUPPLIED: do not use) |
| `web_zip` | VARCHAR | 1 distinct; length 5-5 | values: `31904` | constant in this data |
| `web_country` | VARCHAR | 1 distinct; length 13-13 | values: `United States` | constant in this data |
| `web_gmt_offset` | DECIMAL(5,2) | 1 distinct; -5.00 to -5.00 | values: `-5.0` | constant in this data |
| `web_tax_percentage` | DECIMAL(5,2) | 1 distinct; 0.10 to 0.10 | values: `0.1` | constant in this data |

## Joins

No foreign keys are declared; these were inferred from column names and confirmed against the data.

- `call_center.cc_city` -> `store.s_city`
- `call_center.cc_city` -> `warehouse.w_city`
- `call_center.cc_city` -> `web_site.web_city`
- `call_center.cc_closed_date_sk` -> `date_dim.d_date_sk`
- `call_center.cc_closed_date_sk` -> `store.s_closed_date_sk`
- `call_center.cc_company_name` -> `web_site.web_company_name`
- `call_center.cc_country` -> `store.s_country`
- `call_center.cc_country` -> `warehouse.w_country`
- `call_center.cc_country` -> `web_site.web_country`
- `call_center.cc_county` -> `store.s_county`
- `call_center.cc_county` -> `warehouse.w_county`
- `call_center.cc_county` -> `web_site.web_county`
- `call_center.cc_gmt_offset` -> `store.s_gmt_offset`
- `call_center.cc_gmt_offset` -> `warehouse.w_gmt_offset`
- `call_center.cc_gmt_offset` -> `web_site.web_gmt_offset`
- `call_center.cc_hours` -> `store.s_hours`
- `call_center.cc_open_date_sk` -> `date_dim.d_date_sk`
- `call_center.cc_rec_end_date` -> `date_dim.d_date`
- `call_center.cc_rec_start_date` -> `date_dim.d_date`
- `call_center.cc_state` -> `store.s_state`
- `call_center.cc_state` -> `warehouse.w_state`
- `call_center.cc_state` -> `web_site.web_state`
- `call_center.cc_zip` -> `store.s_zip`
- `call_center.cc_zip` -> `warehouse.w_zip`
- `call_center.cc_zip` -> `web_site.web_zip`
- `catalog_page.cp_end_date_sk` -> `date_dim.d_date_sk`
- `catalog_page.cp_start_date_sk` -> `date_dim.d_date_sk`
- `catalog_returns.cr_call_center_sk` -> `call_center.cc_call_center_sk`
- `catalog_returns.cr_catalog_page_sk` -> `catalog_page.cp_catalog_page_sk`
- `catalog_returns.cr_item_sk` -> `item.i_item_sk`
- `catalog_returns.cr_reason_sk` -> `reason.r_reason_sk`
- `catalog_returns.cr_refunded_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_returns.cr_refunded_customer_sk` -> `customer.c_customer_sk`
- `catalog_returns.cr_refunded_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_returns.cr_refunded_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `catalog_returns.cr_returned_date_sk` -> `date_dim.d_date_sk`
- `catalog_returns.cr_returned_time_sk` -> `time_dim.t_time_sk`
- `catalog_returns.cr_returning_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_returns.cr_returning_customer_sk` -> `customer.c_customer_sk`
- `catalog_returns.cr_returning_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_returns.cr_returning_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `catalog_returns.cr_ship_mode_sk` -> `ship_mode.sm_ship_mode_sk`
- `catalog_returns.cr_warehouse_sk` -> `warehouse.w_warehouse_sk`
- `catalog_sales.cs_bill_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_sales.cs_bill_customer_sk` -> `customer.c_customer_sk`
- `catalog_sales.cs_bill_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_sales.cs_bill_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `catalog_sales.cs_call_center_sk` -> `call_center.cc_call_center_sk`
- `catalog_sales.cs_catalog_page_sk` -> `catalog_page.cp_catalog_page_sk`
- `catalog_sales.cs_item_sk` -> `item.i_item_sk`
- `catalog_sales.cs_promo_sk` -> `promotion.p_promo_sk`
- `catalog_sales.cs_ship_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_sales.cs_ship_customer_sk` -> `customer.c_customer_sk`
- `catalog_sales.cs_ship_date_sk` -> `date_dim.d_date_sk`
- `catalog_sales.cs_ship_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `catalog_sales.cs_ship_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `catalog_sales.cs_ship_mode_sk` -> `ship_mode.sm_ship_mode_sk`
- `catalog_sales.cs_sold_date_sk` -> `date_dim.d_date_sk`
- `catalog_sales.cs_sold_time_sk` -> `time_dim.t_time_sk`
- `catalog_sales.cs_warehouse_sk` -> `warehouse.w_warehouse_sk`
- `customer.c_current_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `customer.c_current_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `customer.c_current_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `customer.c_first_sales_date_sk` -> `date_dim.d_date_sk`
- `customer.c_first_shipto_date_sk` -> `date_dim.d_date_sk`
- `customer.c_last_review_date_sk` -> `date_dim.d_date_sk`
- `customer_address.ca_country` -> `call_center.cc_country`
- `customer_address.ca_country` -> `store.s_country`
- `customer_address.ca_country` -> `warehouse.w_country`
- `customer_address.ca_country` -> `web_site.web_country`
- `household_demographics.hd_demo_sk` -> `customer_demographics.cd_demo_sk`
- `household_demographics.hd_income_band_sk` -> `income_band.ib_income_band_sk`
- `inventory.inv_date_sk` -> `date_dim.d_date_sk`
- `inventory.inv_item_sk` -> `item.i_item_sk`
- `inventory.inv_warehouse_sk` -> `warehouse.w_warehouse_sk`
- `item.i_rec_end_date` -> `date_dim.d_date`
- `item.i_rec_start_date` -> `date_dim.d_date`
- `promotion.p_end_date_sk` -> `date_dim.d_date_sk`
- `promotion.p_item_sk` -> `item.i_item_sk`
- `promotion.p_start_date_sk` -> `date_dim.d_date_sk`
- `store.s_city` -> `call_center.cc_city`
- `store.s_city` -> `warehouse.w_city`
- `store.s_city` -> `web_site.web_city`
- `store.s_closed_date_sk` -> `date_dim.d_date_sk`
- `store.s_country` -> `call_center.cc_country`
- `store.s_country` -> `warehouse.w_country`
- `store.s_country` -> `web_site.web_country`
- `store.s_county` -> `call_center.cc_county`
- `store.s_county` -> `warehouse.w_county`
- `store.s_county` -> `web_site.web_county`
- `store.s_geography_class` -> `web_site.web_class`
- `store.s_gmt_offset` -> `call_center.cc_gmt_offset`
- `store.s_gmt_offset` -> `warehouse.w_gmt_offset`
- `store.s_gmt_offset` -> `web_site.web_gmt_offset`
- `store.s_hours` -> `call_center.cc_hours`
- `store.s_rec_end_date` -> `date_dim.d_date`
- `store.s_rec_start_date` -> `date_dim.d_date`
- `store.s_state` -> `call_center.cc_state`
- `store.s_state` -> `warehouse.w_state`
- `store.s_state` -> `web_site.web_state`
- `store.s_zip` -> `call_center.cc_zip`
- `store.s_zip` -> `warehouse.w_zip`
- `store.s_zip` -> `web_site.web_zip`
- `store_returns.sr_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `store_returns.sr_customer_sk` -> `customer.c_customer_sk`
- `store_returns.sr_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `store_returns.sr_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `store_returns.sr_item_sk` -> `item.i_item_sk`
- `store_returns.sr_reason_sk` -> `reason.r_reason_sk`
- `store_returns.sr_return_time_sk` -> `time_dim.t_time_sk`
- `store_returns.sr_returned_date_sk` -> `date_dim.d_date_sk`
- `store_returns.sr_store_sk` -> `store.s_store_sk`
- `store_sales.ss_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `store_sales.ss_customer_sk` -> `customer.c_customer_sk`
- `store_sales.ss_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `store_sales.ss_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `store_sales.ss_item_sk` -> `item.i_item_sk`
- `store_sales.ss_promo_sk` -> `promotion.p_promo_sk`
- `store_sales.ss_sold_date_sk` -> `date_dim.d_date_sk`
- `store_sales.ss_sold_time_sk` -> `time_dim.t_time_sk`
- `store_sales.ss_store_sk` -> `store.s_store_sk`
- `warehouse.w_city` -> `call_center.cc_city`
- `warehouse.w_city` -> `store.s_city`
- `warehouse.w_city` -> `web_site.web_city`
- `warehouse.w_country` -> `call_center.cc_country`
- `warehouse.w_country` -> `store.s_country`
- `warehouse.w_country` -> `web_site.web_country`
- `warehouse.w_county` -> `call_center.cc_county`
- `warehouse.w_county` -> `store.s_county`
- `warehouse.w_county` -> `web_site.web_county`
- `warehouse.w_gmt_offset` -> `call_center.cc_gmt_offset`
- `warehouse.w_gmt_offset` -> `store.s_gmt_offset`
- `warehouse.w_gmt_offset` -> `web_site.web_gmt_offset`
- `warehouse.w_state` -> `call_center.cc_state`
- `warehouse.w_state` -> `store.s_state`
- `warehouse.w_state` -> `web_site.web_state`
- `warehouse.w_zip` -> `call_center.cc_zip`
- `warehouse.w_zip` -> `store.s_zip`
- `warehouse.w_zip` -> `web_site.web_zip`
- `web_page.wp_access_date_sk` -> `date_dim.d_date_sk`
- `web_page.wp_creation_date_sk` -> `date_dim.d_date_sk`
- `web_page.wp_customer_sk` -> `customer.c_customer_sk`
- `web_page.wp_rec_end_date` -> `date_dim.d_date`
- `web_page.wp_rec_start_date` -> `date_dim.d_date`
- `web_returns.wr_item_sk` -> `item.i_item_sk`
- `web_returns.wr_reason_sk` -> `reason.r_reason_sk`
- `web_returns.wr_refunded_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_returns.wr_refunded_customer_sk` -> `customer.c_customer_sk`
- `web_returns.wr_refunded_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_returns.wr_refunded_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `web_returns.wr_returned_date_sk` -> `date_dim.d_date_sk`
- `web_returns.wr_returned_time_sk` -> `time_dim.t_time_sk`
- `web_returns.wr_returning_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_returns.wr_returning_customer_sk` -> `customer.c_customer_sk`
- `web_returns.wr_returning_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_returns.wr_returning_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `web_returns.wr_web_page_sk` -> `web_page.wp_web_page_sk`
- `web_sales.ws_bill_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_sales.ws_bill_customer_sk` -> `customer.c_customer_sk`
- `web_sales.ws_bill_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_sales.ws_bill_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `web_sales.ws_item_sk` -> `item.i_item_sk`
- `web_sales.ws_promo_sk` -> `promotion.p_promo_sk`
- `web_sales.ws_ship_cdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_sales.ws_ship_customer_sk` -> `customer.c_customer_sk`
- `web_sales.ws_ship_date_sk` -> `date_dim.d_date_sk`
- `web_sales.ws_ship_hdemo_sk` -> `customer_demographics.cd_demo_sk`
- `web_sales.ws_ship_hdemo_sk` -> `household_demographics.hd_demo_sk`
- `web_sales.ws_ship_mode_sk` -> `ship_mode.sm_ship_mode_sk`
- `web_sales.ws_sold_date_sk` -> `date_dim.d_date_sk`
- `web_sales.ws_sold_time_sk` -> `time_dim.t_time_sk`
- `web_sales.ws_warehouse_sk` -> `warehouse.w_warehouse_sk`
- `web_sales.ws_web_page_sk` -> `web_page.wp_web_page_sk`
- `web_sales.ws_web_site_sk` -> `web_site.web_site_sk`
- `web_site.web_city` -> `call_center.cc_city`
- `web_site.web_city` -> `store.s_city`
- `web_site.web_city` -> `warehouse.w_city`
- `web_site.web_close_date_sk` -> `date_dim.d_date_sk`
- `web_site.web_company_name` -> `call_center.cc_company_name`
- `web_site.web_country` -> `call_center.cc_country`
- `web_site.web_country` -> `store.s_country`
- `web_site.web_country` -> `warehouse.w_country`
- `web_site.web_county` -> `call_center.cc_county`
- `web_site.web_county` -> `store.s_county`
- `web_site.web_county` -> `warehouse.w_county`
- `web_site.web_gmt_offset` -> `call_center.cc_gmt_offset`
- `web_site.web_gmt_offset` -> `store.s_gmt_offset`
- `web_site.web_gmt_offset` -> `warehouse.w_gmt_offset`
- `web_site.web_open_date_sk` -> `date_dim.d_date_sk`
- `web_site.web_rec_end_date` -> `date_dim.d_date`
- `web_site.web_rec_start_date` -> `date_dim.d_date`
- `web_site.web_state` -> `call_center.cc_state`
- `web_site.web_state` -> `store.s_state`
- `web_site.web_state` -> `warehouse.w_state`
- `web_site.web_zip` -> `call_center.cc_zip`
- `web_site.web_zip` -> `store.s_zip`
- `web_site.web_zip` -> `warehouse.w_zip`
