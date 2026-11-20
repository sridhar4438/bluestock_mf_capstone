import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
dim = pd.read_sql_query(
    "SELECT amfi_code, scheme_name, category, risk_category, expense_ratio_pct FROM dim_fund",
    conn
)
conn.close()
dim["amfi_code"] = dim["amfi_code"].astype(str)

# Our calculated Sharpe, from the scorecard (not the provided file)
score = pd.read_csv(BASE / "Data" / "processed" / "fund_scorecard.csv",
                    dtype={"amfi_code": str})
fund = dim.merge(score[["amfi_code", "sharpe", "cagr_3yr_pct", "score"]], on="amfi_code")

RISK_LEVELS = ["Low", "Moderate", "Moderately High", "High", "Very High"]

def recommend(risk_appetite, top_n=3):
    """Top funds by our calculated Sharpe ratio within a risk category."""
    matches = fund[fund["risk_category"].str.lower() == risk_appetite.lower()]
    if matches.empty:
        return pd.DataFrame()
    return (matches.sort_values("sharpe", ascending=False)
                   .head(top_n)
                   [["scheme_name", "category", "risk_category",
                     "sharpe", "cagr_3yr_pct", "expense_ratio_pct"]])

if __name__ == "__main__":
    print("Risk categories in the data:")
    print(fund["risk_category"].value_counts())
    print()
    for level in RISK_LEVELS:
        print(f"Top 3 for {level} risk appetite:")
        table = recommend(level)
        print(table.to_string(index=False) if not table.empty else "  (no funds in this category)")
        print()