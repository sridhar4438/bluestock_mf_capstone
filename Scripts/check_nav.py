from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "Data" / "raw"

nav = pd.read_csv(next(RAW_DIR.glob("*nav_history*.csv")))

print("Rows:", len(nav))
print()
print("Data types:")
print(nav.dtypes)
print()
print("Empty cells per column:")
print(nav.isnull().sum())
print()
print("Duplicate rows:", nav.duplicated().sum())
print("Duplicate fund+date pairs:", nav.duplicated(subset=["amfi_code", "date"]).sum())
print("NAV values <= 0:", (nav["nav"] <= 0).sum())
print()
print("Date range:", nav["date"].min(), "to", nav["date"].max())