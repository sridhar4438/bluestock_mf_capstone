import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "Data" / "processed"

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
nav = pd.read_sql_query(
    "SELECT amfi_code, date, nav FROM fact_nav ORDER BY amfi_code, date",
    conn, parse_dates=["date"]
)
dim = pd.read_sql_query("SELECT amfi_code, scheme_name, category FROM dim_fund", conn)
conn.close()

nav["amfi_code"] = nav["amfi_code"].astype(str)
dim["amfi_code"] = dim["amfi_code"].astype(str)
nav["r"] = nav.groupby("amfi_code")["nav"].pct_change()

rows = []
for code, g in nav.groupby("amfi_code"):
    r = g["r"].dropna()
    var_95 = np.percentile(r, 5)            # 5th percentile of daily returns
    cvar_95 = r[r <= var_95].mean()         # average of the worst 5% of days
    rows.append({
        "amfi_code": code,
        "var_95_daily_pct": round(var_95 * 100, 3),
        "cvar_95_daily_pct": round(cvar_95 * 100, 3),
    })

res = pd.DataFrame(rows).merge(dim, on="amfi_code")
res = res[["amfi_code", "scheme_name", "category",
           "var_95_daily_pct", "cvar_95_daily_pct"]]
res = res.sort_values("var_95_daily_pct")

print("Average by category (daily %):")
print(res.groupby("category")[["var_95_daily_pct", "cvar_95_daily_pct"]].mean().round(3))
print()
print("Worst 5 funds:")
print(res.head(5).to_string(index=False))
print()

res.to_csv(PROC / "var_cvar_report.csv", index=False)
print("Saved to Data/processed/var_cvar_report.csv")