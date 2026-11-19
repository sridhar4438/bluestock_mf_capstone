from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "Data" / "raw"

tx = pd.read_csv(next(RAW_DIR.glob("*investor_transactions*.csv")))

print("Rows:", len(tx))
print()
print("Empty cells per column:")
print(tx.isnull().sum())
print()
print("Duplicate rows:", tx.duplicated().sum())
print()
print("Transaction types:")
print(tx["transaction_type"].value_counts(dropna=False))
print()
print("KYC status:")
print(tx["kyc_status"].value_counts(dropna=False))
print()
print("Amount <= 0:", (tx["amount_inr"] <= 0).sum())
print("Amount min / max:", tx["amount_inr"].min(), "/", tx["amount_inr"].max())
print()
bad_dates = pd.to_datetime(tx["transaction_date"], errors="coerce").isnull().sum()
print("Bad dates:", bad_dates)
print()
print("City tiers:")
print(tx["city_tier"].value_counts(dropna=False))
print("Age groups:")
print(tx["age_group"].value_counts(dropna=False))