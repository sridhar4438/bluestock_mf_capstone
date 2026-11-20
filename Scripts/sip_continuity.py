import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "Data" / "processed"

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
sip = pd.read_sql_query(
    "SELECT investor_id, transaction_date FROM fact_transactions "
    "WHERE transaction_type = 'SIP'",
    conn, parse_dates=["transaction_date"]
)
conn.close()

sip = sip.sort_values(["investor_id", "transaction_date"])
sip["gap_days"] = sip.groupby("investor_id")["transaction_date"].diff().dt.days

# Keep only investors with 6 or more SIPs
counts = sip.groupby("investor_id").size()
eligible = counts[counts >= 6].index
s = sip[sip["investor_id"].isin(eligible)]

per_investor = s.groupby("investor_id").agg(
    sip_count=("transaction_date", "size"),
    avg_gap_days=("gap_days", "mean"),
).reset_index()
per_investor["at_risk"] = per_investor["avg_gap_days"] > 35

print("Investors with 6+ SIPs:", len(per_investor))
print("At-risk investors (avg gap > 35 days):", per_investor["at_risk"].sum())
print("Share at risk:", round(per_investor["at_risk"].mean() * 100, 1), "%")
print()
print("Average gap (days):", round(per_investor["avg_gap_days"].mean(), 1))
print("Median gap (days):", round(per_investor["avg_gap_days"].median(), 1))
print()
print(per_investor.head(10).round(1).to_string(index=False))

per_investor.round(2).to_csv(PROC / "sip_continuity.csv", index=False)
print("\nSaved to Data/processed/sip_continuity.csv")