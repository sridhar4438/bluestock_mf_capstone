import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
CHART_DIR = BASE / "Reports" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
nav = pd.read_sql_query(
    "SELECT amfi_code, date, nav FROM fact_nav ORDER BY amfi_code, date",
    conn, parse_dates=["date"]
)
dim = pd.read_sql_query("SELECT amfi_code, scheme_name, category FROM dim_fund", conn)
conn.close()
nav["amfi_code"] = nav["amfi_code"].astype(str)
dim["amfi_code"] = dim["amfi_code"].astype(str)

# Pick the top equity fund and two others from the scorecard
score = pd.read_csv(BASE / "Data" / "processed" / "fund_scorecard.csv", dtype={"amfi_code": str})
top_eq = score[score["category"] == "Equity"].head(3)
top_debt = score[score["category"] == "Debt"].head(1)
picked = pd.concat([top_eq, top_debt])
codes = picked["amfi_code"].tolist()
names = dict(zip(picked["amfi_code"], picked["scheme_name"].str.split(" - ").str[0]))

wide = nav[nav["amfi_code"].isin(codes)].copy()
wide["r"] = wide.groupby("amfi_code")["nav"].pct_change()
rets = wide.pivot(index="date", columns="amfi_code", values="r").dropna()

# Rolling 90-day Sharpe, annualised, with the same 6.5% risk-free rate
RF_DAILY = 0.065 / 252
roll = rets.rolling(90)
rolling_sharpe = (roll.mean() - RF_DAILY) / roll.std() * np.sqrt(252)
rolling_sharpe = rolling_sharpe.dropna()

fig, ax = plt.subplots(figsize=(12, 6))
for c in codes:
    ax.plot(rolling_sharpe.index, rolling_sharpe[c], linewidth=1, label=names[c])
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Rolling 90-Day Sharpe Ratio (annualised)")
ax.set_xlabel("Date")
ax.set_ylabel("Sharpe ratio")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.savefig(CHART_DIR / "13_rolling_sharpe.png", dpi=150, bbox_inches="tight")
plt.show()

print("Latest rolling Sharpe:")
print(rolling_sharpe.iloc[-1].round(2).rename(lambda c: names[c]))
print("Average over the period:")
print(rolling_sharpe.mean().round(2).rename(lambda c: names[c]))