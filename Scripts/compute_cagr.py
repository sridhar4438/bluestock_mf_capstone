import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(BASE_DIR / "Data" / "db" / "bluestock_mf.db")

nav = pd.read_sql_query(
    "SELECT amfi_code, date, nav FROM fact_nav ORDER BY amfi_code, date",
    conn, parse_dates=["date"]
)
nav["amfi_code"] = nav["amfi_code"].astype(str)

# Windows in trading days (252 trading days = 1 year)
WINDOWS = {"1yr": 252, "3yr": 756, "5yr": 1260}

rows = []
for code, g in nav.groupby("amfi_code"):
    prices = g["nav"].to_numpy()
    row = {"amfi_code": code}
    for label, days in WINDOWS.items():
        if len(prices) > days:
            start, end = prices[-1 - days], prices[-1]
            years = days / 252
            row[f"cagr_{label}_pct"] = round(((end / start) ** (1 / years) - 1) * 100, 2)
        else:
            row[f"cagr_{label}_pct"] = np.nan   # not enough history
    rows.append(row)

cagr = pd.DataFrame(rows)
cagr.to_csv(BASE_DIR / "Data" / "processed" / "cagr_report.csv", index=False)

print("Funds with a 5yr CAGR:", cagr["cagr_5yr_pct"].notna().sum(),
      "(0 means not enough history)")
print(cagr.describe().round(2))
print("\nSaved to Data/processed/cagr_report.csv")

conn.close()