import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROC_DIR = BASE_DIR / "Data" / "processed"
DB_DIR = BASE_DIR / "Data" / "db"
SCHEMA = BASE_DIR / "SQL" / "schema.sql"

DB_DIR.mkdir(parents=True, exist_ok=True)
db_path = DB_DIR / "bluestock_mf.db"
if db_path.exists():
    db_path.unlink()          # start fresh every time

# table name, csv file, columns that hold dates
tables = [
    ("dim_fund",              "clean_fund_master.csv",      ["launch_date"]),
    ("fact_nav",              "clean_nav.csv",              ["date"]),
    ("fact_transactions",     "clean_transactions.csv",     ["transaction_date"]),
    ("fact_performance",      "clean_performance.csv",      []),
    ("fact_portfolio",        "clean_holdings.csv",         ["portfolio_date"]),
    ("fact_aum",              "clean_aum.csv",              ["date"]),
    ("fact_sip_industry",     "clean_sip_inflows.csv",      []),
    ("fact_category_inflows", "clean_category_inflows.csv", []),
    ("fact_folio_count",      "clean_folio_count.csv",      []),
    ("fact_benchmark",        "clean_benchmarks.csv",       ["date"]),
]

conn = sqlite3.connect(db_path)
conn.executescript(SCHEMA.read_text())     # build the empty tables

for table, csv_name, date_cols in tables:
    df = pd.read_csv(PROC_DIR / csv_name, dtype={"amfi_code": str})
    for col in date_cols:
        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
    df.to_sql(table, conn, if_exists="append", index=False)
    print(f"{table}: {len(df)} rows loaded")

# Safety check: do all transaction fund codes exist in dim_fund?
orphans = conn.execute("""
    SELECT COUNT(*) FROM fact_transactions
    WHERE amfi_code NOT IN (SELECT amfi_code FROM dim_fund)
""").fetchone()[0]
print("Transactions with unknown fund code:", orphans)

conn.commit()
conn.close()
print("Database saved to Data/db/bluestock_mf.db")