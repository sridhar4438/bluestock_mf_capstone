from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data" / "raw"
OUT_DIR = BASE_DIR / "Data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

nav = pd.read_csv(next(RAW_DIR.glob("*nav_history*.csv")))

# 1. Make dates real dates, make codes text
nav["date"] = pd.to_datetime(nav["date"])
nav["amfi_code"] = nav["amfi_code"].astype(str)

# 2. Sort by fund, then by date
nav = nav.sort_values(["amfi_code", "date"])

# 3. Fill holiday gaps fund by fund
cleaned = []
for code, group in nav.groupby("amfi_code"):
    group = group.set_index("date")
    all_days = pd.date_range(group.index.min(), group.index.max(), freq="B")
    group = group.reindex(all_days)
    group["nav"] = group["nav"].ffill()
    group["amfi_code"] = code
    group = group.rename_axis("date").reset_index()
    cleaned.append(group)

clean_nav = pd.concat(cleaned, ignore_index=True)

# 4. Daily return in percent, calculated within each fund
clean_nav["daily_return_pct"] = (
    clean_nav.groupby("amfi_code")["nav"].pct_change() * 100
)

print("Rows before:", len(nav))
print("Rows after:", len(clean_nav))
print("Holiday rows filled:", len(clean_nav) - len(nav))
print(clean_nav.head())

clean_nav.to_csv(OUT_DIR / "clean_nav.csv", index=False)
print("Saved to Data/processed/clean_nav.csv")