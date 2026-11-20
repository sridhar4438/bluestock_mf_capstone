import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "Data" / "processed"

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
hold = pd.read_sql_query(
    """
    SELECT h.amfi_code, h.sector, h.weight_pct, f.scheme_name, f.category
    FROM fact_portfolio h
    JOIN dim_fund f ON f.amfi_code = h.amfi_code
    WHERE f.category = 'Equity'
    """,
    conn
)
conn.close()

# Total weight in each sector for each fund
sector_w = (hold.groupby(["amfi_code", "scheme_name", "sector"])["weight_pct"]
                .sum().reset_index())

# HHI = sum of squared sector weights
hhi = (sector_w.assign(sq=lambda d: d["weight_pct"] ** 2)
               .groupby(["amfi_code", "scheme_name"])
               .agg(sectors=("sector", "nunique"),
                    total_weight_pct=("weight_pct", "sum"),
                    hhi=("sq", "sum"))
               .reset_index()
               .sort_values("hhi", ascending=False))
hhi["hhi"] = hhi["hhi"].round(0)
hhi["total_weight_pct"] = hhi["total_weight_pct"].round(1)

print("Equity funds with holdings:", len(hhi))
print("Average HHI:", round(hhi["hhi"].mean()))
print("Median HHI:", round(hhi["hhi"].median()))
print()
print("Most concentrated 5:")
print(hhi.head(5).to_string(index=False))
print()
print("Least concentrated 5:")
print(hhi.tail(5).to_string(index=False))

hhi.to_csv(PROC / "sector_hhi.csv", index=False)
print("\nSaved to Data/processed/sector_hhi.csv")