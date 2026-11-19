from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "Data" / "raw"

fund_master = pd.read_csv(next(RAW_DIR.glob("*fund_master*.csv")))
nav_history = pd.read_csv(next(RAW_DIR.glob("*nav_history*.csv")))

master_codes = set(fund_master["amfi_code"].astype(str))
nav_codes = set(nav_history["amfi_code"].astype(str))

missing = master_codes - nav_codes
extra = nav_codes - master_codes

print("Funds in master:", len(master_codes))
print("Funds in NAV history:", len(nav_codes))
print("In master but missing NAV:", missing if missing else "None")
print("In NAV but not in master:", extra if extra else "None")

print()
print("Fund houses:", fund_master["fund_house"].nunique())
print(fund_master["category"].value_counts())