import sqlite3
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "dashboard" / "data"
OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(BASE / "Data" / "db" / "bluestock_mf.db")
tables = ["dim_fund", "fact_nav", "fact_transactions", "fact_performance",
          "fact_portfolio", "fact_aum", "fact_sip_industry",
          "fact_category_inflows", "fact_folio_count", "fact_benchmark"]

for t in tables:
    pd.read_sql_query(f"SELECT * FROM {t}", conn).to_csv(OUT / f"{t}.csv", index=False)
    print("exported", t)

conn.close()
print("Done. Files in dashboard/data")