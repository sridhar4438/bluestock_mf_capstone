# Bluestock Mutual Fund Analytics Platform

An end-to-end data project covering the full pipeline for Indian mutual fund data: ingestion, cleaning, a SQLite database, exploratory analysis, performance and risk metrics, advanced analytics, and a four-page Power BI dashboard.

Built as an individual capstone for Bluestock Fintech (7 working days).

## Project structure

```
bluestock_mf_capstone/
├── Data/
│   ├── raw/          Original 10 CSV datasets (not modified)
│   ├── processed/    Cleaned CSVs and computed metrics
│   └── db/           bluestock_mf.db (SQLite, not committed to GitHub)
├── Notebooks/        03_eda_analysis.ipynb, 04_performance_analytics.ipynb, 06_advanced_analytics.ipynb
├── Scripts/          Cleaning, metrics and analysis scripts
├── SQL/              schema.sql (10 tables) and queries.sql (10 queries)
├── Reports/charts/   Chart images from the EDA and analytics notebooks
├── dashboard/        Power BI file and the CSVs it reads
├── run_pipeline.py   Runs the data and metrics pipeline in order
└── data_dictionary.md
```

## Setup

Requires Python 3.10 or newer.

```bash
pip install -r requirements.txt
```

## How to run

1. Place the 10 raw CSV files in `Data/raw/`.
2. Run the pipeline from the project folder:
   ```bash
   python run_pipeline.py
   ```
   This cleans the data, builds `Data/db/bluestock_mf.db`, and computes returns, CAGR, risk, scorecard, VaR, sector concentration, investor cohorts, SIP continuity and the fund recommender.
3. Open the notebooks in `Notebooks/` and choose **Run All** to regenerate the charts in `Reports/charts/`.
4. Open `dashboard/bluestock_mf_dashboard.pbix` in Power BI Desktop. The dashboard reads CSVs exported with `Scripts/export_for_powerbi.py`.

## Key outputs

| Output | Location |
|---|---|
| Cleaned data | `Data/processed/` |
| Database | `Data/db/bluestock_mf.db` |
| Fund scorecard | `Data/processed/fund_scorecard.csv` |
| Risk metrics (VaR, CVaR) | `Data/processed/var_cvar_report.csv` |
| Charts | `Reports/charts/` |
| Dashboard | `dashboard/bluestock_mf_dashboard.pbix` |

## Data and limitations

The data is provided as part of the Bluestock capstone. Several checks showed that the dataset behaves unlike real market data, and the analysis reports these as limitations rather than findings:

- **Fund returns are almost uncorrelated** (about -0.08 to +0.05 between funds), while real equity funds move together strongly. The same holds for the benchmark indices, where the Nifty 50 and Nifty 100 have a daily correlation of about -0.05.
- **Beta and R-squared are close to zero** for every fund, so market-relative measures (Alpha, Beta, tracking error) are not meaningful here.
- **The provided `scheme_performance` file does not match** returns calculated from the NAV history (average gap about 15 percentage points for 1-year returns). Calculated values are used throughout.
- **5-year CAGR cannot be computed**, because the NAV history covers about 4.6 years.
- **Investor transactions start in January 2024**, so there are no earlier investor cohorts, and the at-risk SIP flag reflects irregular simulated dates rather than real behaviour.
- **Each fund holds only about 6 to 10 stocks** in the holdings data.
- **Fund codes**: at least one code in the project PDF (125497) is labelled differently from the live mfapi.in name, so fund names were taken from the data itself.

## Methods

- **Returns:** daily percentage change in NAV; annualised with 252 trading days.
- **CAGR:** compound annual growth over 1 and 3 years.
- **Sharpe ratio:** (annualised return − 6.5%) ÷ annualised volatility, with the 6.5% risk-free proxy from the project brief.
- **Sortino, alpha, beta and drawdown:** computed from the NAV history.
- **Scorecard:** percentile ranks within each category, weighted 30% 3-year return, 25% Sharpe, 20% alpha, 15% expense ratio and 10% maximum drawdown.
- **VaR and CVaR:** 5th percentile of daily returns and the mean of returns at or below it.
- **HHI:** sum of squared sector weights per fund.
- **Recommender:** top 3 funds by calculated Sharpe within each risk grade. Rule-based, not personalised advice.

## Disclaimer

This project is for educational purposes only and is not financial advice. Mutual fund investments are subject to market risks.

## Author

Sridhar, Bluestock Fintech capstone.