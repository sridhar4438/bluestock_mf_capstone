from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROC = BASE / "Data" / "processed"
RISK_FREE = 6.5   # % per year, the PDF's proxy

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")

# 1. Fund details
dim = pd.read_sql_query(
    "SELECT amfi_code, scheme_name, category, expense_ratio_pct FROM dim_fund", conn
)
dim["amfi_code"] = dim["amfi_code"].astype(str)

# 2. Annual return and risk, calculated from the NAV history
nav = pd.read_sql_query(
    "SELECT amfi_code, date, nav FROM fact_nav ORDER BY amfi_code, date",
    conn, parse_dates=["date"]
)
conn.close()
nav["amfi_code"] = nav["amfi_code"].astype(str)
nav["r"] = nav.groupby("amfi_code")["nav"].pct_change()

rows = []
for code, g in nav.groupby("amfi_code"):
    r = g["r"].dropna()
    n = len(r)
    rows.append({
        "amfi_code": code,
        "annualised_return_pct": ((1 + r).prod() ** (252 / n) - 1) * 100,
        "annualised_risk_pct": r.std() * np.sqrt(252) * 100,
    })
ret = pd.DataFrame(rows)

# 3. Other metrics from the files we already saved
cagr = pd.read_csv(PROC / "cagr_report.csv", dtype={"amfi_code": str})
ab = pd.read_csv(PROC / "alpha_beta.csv", dtype={"amfi_code": str})
dd = pd.read_csv(PROC / "max_drawdown.csv", dtype={"amfi_code": str})

# 4. Combine everything
df = (dim.merge(ret, on="amfi_code")
         .merge(cagr[["amfi_code", "cagr_3yr_pct"]], on="amfi_code")
         .merge(ab[["amfi_code", "alpha_ann_pct"]], on="amfi_code")
         .merge(dd[["amfi_code", "max_drawdown_pct"]], on="amfi_code"))
print("Funds combined:", len(df))

df["sharpe"] = (df["annualised_return_pct"] - RISK_FREE) / df["annualised_risk_pct"]

# 5. Score within each category (0 to 1, higher is better)
df["r_return"] = df.groupby("category")["cagr_3yr_pct"].rank(pct=True)
df["r_sharpe"] = df.groupby("category")["sharpe"].rank(pct=True)
df["r_alpha"] = df.groupby("category")["alpha_ann_pct"].rank(pct=True)
df["r_expense"] = df.groupby("category")["expense_ratio_pct"].rank(pct=True, ascending=False)
df["r_drawdown"] = df.groupby("category")["max_drawdown_pct"].rank(pct=True)

df["score"] = (100 * (0.30 * df["r_return"] + 0.25 * df["r_sharpe"]
                      + 0.20 * df["r_alpha"] + 0.15 * df["r_expense"]
                      + 0.10 * df["r_drawdown"])).round(1)

df = df.sort_values(["category", "score"], ascending=[True, False])
keep = ["category", "scheme_name", "amfi_code", "score", "cagr_3yr_pct",
        "sharpe", "alpha_ann_pct", "expense_ratio_pct", "max_drawdown_pct"]
df[keep].to_csv(PROC / "fund_scorecard.csv", index=False)

for cat, g in df.groupby("category"):
    print(f"\nTop 5 in {cat}:")
    print(g[["scheme_name", "score", "cagr_3yr_pct", "sharpe"]].head(5).round(2).to_string(index=False))

print("\nSaved to Data/processed/fund_scorecard.csv")