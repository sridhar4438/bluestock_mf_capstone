import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(BASE_DIR / "Data" / "db" / "bluestock_mf.db")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

text = (BASE_DIR / "SQL" / "queries.sql").read_text()

for chunk in text.split(";"):
    lines = [l for l in chunk.strip().splitlines() if l.strip()]
    if not lines:
        continue
    title = lines[0]
    sql = "\n".join(lines[1:])
    print("=" * 70)
    print(title)
    print(pd.read_sql_query(sql, conn).to_string(index=False))
    print()

conn.close()