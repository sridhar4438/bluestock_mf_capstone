import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "Data" / "processed"

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
tx = pd.read_sql_query(
    """
    SELECT t.investor_id, t.transaction_date, t.transaction_type,
           t.amount_inr, t.amfi_code, f.category
    FROM fact_transactions t
    JOIN dim_fund f ON f.amfi_code = t.amfi_code
    """,
    conn, parse_dates=["transaction_date"]
)
conn.close()

# Each investor's first transaction year = their cohort
tx["year"] = tx["transaction_date"].dt.year
first_year = tx.groupby("investor_id")["year"].min().rename("cohort")
tx = tx.merge(first_year, on="investor_id")

# Cohort summary
investors = tx.groupby("cohort")["investor_id"].nunique().rename("investors")
sips = tx[tx["transaction_type"] == "SIP"]
avg_sip = sips.groupby("cohort")["amount_inr"].mean().rename("avg_sip_inr")
total_inv = tx[tx["transaction_type"] != "Redemption"].groupby("cohort")["amount_inr"].sum() / 1e7
total_inv = total_inv.rename("invested_crore")
debt_share = (tx[tx["transaction_type"] != "Redemption"]
              .assign(is_debt=lambda d: d["category"] == "Debt")
              .groupby("cohort")
              .apply(lambda d: d.loc[d["is_debt"], "amount_inr"].sum() / d["amount_inr"].sum() * 100,
                     include_groups=False)
              .rename("debt_share_pct"))

summary = pd.concat([investors, avg_sip, total_inv, debt_share], axis=1).round(2)
print(summary)
print()

summary.to_csv(PROC / "investor_cohorts.csv")
print("Saved to Data/processed/investor_cohorts.csv")