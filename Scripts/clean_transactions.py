from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data" / "raw"
OUT_DIR = BASE_DIR / "Data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

tx = pd.read_csv(next(RAW_DIR.glob("*investor_transactions*.csv")))

# 1. Real dates, codes as text
tx["transaction_date"] = pd.to_datetime(tx["transaction_date"])
tx["amfi_code"] = tx["amfi_code"].astype(str)

# 2. Remove stray spaces and fix capitalisation in text columns
text_cols = ["transaction_type", "state", "city", "city_tier",
             "age_group", "gender", "payment_mode", "kyc_status"]
for col in text_cols:
    tx[col] = tx[col].astype(str).str.strip()

tx["transaction_type"] = tx["transaction_type"].replace(
    {"SIP": "SIP", "sip": "SIP", "Lumpsum": "Lumpsum",
     "lumpsum": "Lumpsum", "Redemption": "Redemption", "redemption": "Redemption"}
)

# 3. Keep only valid rows
before = len(tx)
tx = tx[tx["amount_inr"] > 0]
tx = tx.drop_duplicates()
print("Rows removed:", before - len(tx))

# 4. Sort and save
tx = tx.sort_values(["investor_id", "transaction_date"])
tx.to_csv(OUT_DIR / "clean_transactions.csv", index=False)

print("Rows saved:", len(tx))
print(tx.head())
print("Saved to Data/processed/clean_transactions.csv")