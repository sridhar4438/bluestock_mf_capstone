# Data Dictionary

Database: `bluestock_mf.db` (SQLite)

## dim_fund
The 40 mutual fund schemes: name, fund house, category, expense ratio. Source file: `clean_fund_master.csv`. Rows: 40.

| Column | Type |
|---|---|
| amfi_code | TEXT |
| fund_house | TEXT |
| scheme_name | TEXT |
| category | TEXT |
| sub_category | TEXT |
| plan | TEXT |
| launch_date | TEXT |
| benchmark | TEXT |
| expense_ratio_pct | REAL |
| exit_load_pct | REAL |
| min_sip_amount | REAL |
| min_lumpsum_amount | REAL |
| fund_manager | TEXT |
| risk_category | TEXT |
| sebi_category_code | TEXT |

## fact_nav
Daily NAV and daily return for each fund. Source file: `clean_nav.csv`. Rows: 46,000.

| Column | Type |
|---|---|
| amfi_code | TEXT |
| date | TEXT |
| nav | REAL |
| daily_return_pct | REAL |

## fact_transactions
SIP, Lumpsum and Redemption transactions by investors (simulated). Source file: `clean_transactions.csv`. Rows: 32,778.

| Column | Type |
|---|---|
| tx_id | INTEGER |
| investor_id | TEXT |
| transaction_date | TEXT |
| amfi_code | TEXT |
| transaction_type | TEXT |
| amount_inr | INTEGER |
| state | TEXT |
| city | TEXT |
| city_tier | TEXT |
| age_group | TEXT |
| gender | TEXT |
| annual_income_lakh | REAL |
| payment_mode | TEXT |
| kyc_status | TEXT |

## fact_performance
Returns and risk metrics for each fund. Source file: `clean_performance.csv`. Rows: 40.

| Column | Type |
|---|---|
| amfi_code | TEXT |
| scheme_name | TEXT |
| fund_house | TEXT |
| category | TEXT |
| plan | TEXT |
| return_1yr_pct | REAL |
| return_3yr_pct | REAL |
| return_5yr_pct | REAL |
| benchmark_3yr_pct | REAL |
| alpha | REAL |
| beta | REAL |
| sharpe_ratio | REAL |
| sortino_ratio | REAL |
| std_dev_ann_pct | REAL |
| max_drawdown_pct | REAL |
| aum_crore | REAL |
| expense_ratio_pct | REAL |
| morningstar_rating | INTEGER |
| risk_grade | TEXT |
| negative_sharpe_flag | INTEGER |

## fact_portfolio
Top stock holdings of the equity funds. Source file: `clean_holdings.csv`. Rows: 322.

| Column | Type |
|---|---|
| amfi_code | TEXT |
| stock_symbol | TEXT |
| stock_name | TEXT |
| sector | TEXT |
| weight_pct | REAL |
| market_value_cr | REAL |
| current_price_inr | REAL |
| portfolio_date | TEXT |

## fact_aum
Assets under management of 10 fund houses. Source file: `clean_aum.csv`. Rows: 90.

| Column | Type |
|---|---|
| date | TEXT |
| fund_house | TEXT |
| aum_lakh_crore | REAL |
| aum_crore | REAL |
| num_schemes | INTEGER |

## fact_sip_industry
Monthly industry-wide SIP inflows and accounts. Source file: `clean_sip_inflows.csv`. Rows: 48.

| Column | Type |
|---|---|
| month | TEXT |
| sip_inflow_crore | REAL |
| active_sip_accounts_crore | REAL |
| new_sip_accounts_lakh | REAL |
| sip_aum_lakh_crore | REAL |
| yoy_growth_pct | REAL |

## fact_category_inflows
Net inflows by fund category and month. Source file: `clean_category_inflows.csv`. Rows: 144.

| Column | Type |
|---|---|
| month | TEXT |
| category | TEXT |
| net_inflow_crore | REAL |

## fact_folio_count
Industry folio counts by type. Source file: `clean_folio_count.csv`. Rows: 21.

| Column | Type |
|---|---|
| month | TEXT |
| total_folios_crore | REAL |
| equity_folios_crore | REAL |
| debt_folios_crore | REAL |
| hybrid_folios_crore | REAL |
| others_folios_crore | REAL |

## fact_benchmark
Daily closing values of benchmark indices. Source file: `clean_benchmarks.csv`. Rows: 8,050.

| Column | Type |
|---|---|
| date | TEXT |
| index_name | TEXT |
| close_value | REAL |
