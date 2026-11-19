import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(BASE_DIR / "Data" / "db" / "bluestock_mf.db")

about = {
    "dim_fund": ("The 40 mutual fund schemes: name, fund house, category, expense ratio", "clean_fund_master.csv"),
    "fact_nav": ("Daily NAV and daily return for each fund", "clean_nav.csv"),
    "fact_transactions": ("SIP, Lumpsum and Redemption transactions by investors (simulated)", "clean_transactions.csv"),
    "fact_performance": ("Returns and risk metrics for each fund", "clean_performance.csv"),
    "fact_portfolio": ("Top stock holdings of the equity funds", "clean_holdings.csv"),
    "fact_aum": ("Assets under management of 10 fund houses", "clean_aum.csv"),
    "fact_sip_industry": ("Monthly industry-wide SIP inflows and accounts", "clean_sip_inflows.csv"),
    "fact_category_inflows": ("Net inflows by fund category and month", "clean_category_inflows.csv"),
    "fact_folio_count": ("Industry folio counts by type", "clean_folio_count.csv"),
    "fact_benchmark": ("Daily closing values of benchmark indices", "clean_benchmarks.csv"),
}

lines = ["# Data Dictionary", "", "Database: `bluestock_mf.db` (SQLite)", ""]

for table, (description, source) in about.items():
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    lines.append(f"## {table}")
    lines.append(f"{description}. Source file: `{source}`. Rows: {count:,}.")
    lines.append("")
    lines.append("| Column | Type |")
    lines.append("|---|---|")
    for row in conn.execute(f"PRAGMA table_info({table})"):
        lines.append(f"| {row[1]} | {row[2]} |")
    lines.append("")

(BASE_DIR / "data_dictionary.md").write_text("\n".join(lines), encoding="utf-8")
conn.close()
print("data_dictionary.md created")