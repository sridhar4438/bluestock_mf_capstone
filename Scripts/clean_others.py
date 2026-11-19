from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data" / "raw"
OUT_DIR = BASE_DIR / "Data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

files = {
    "fund_master": "clean_fund_master.csv",
    "aum_by_fund_house": "clean_aum.csv",
    "monthly_sip_inflows": "clean_sip_inflows.csv",
    "category_inflows": "clean_category_inflows.csv",
    "industry_folio_count": "clean_folio_count.csv",
    "portfolio_holdings": "clean_holdings.csv",
    "benchmark_indices": "clean_benchmarks.csv",
}

for key, out_name in files.items():
    df = pd.read_csv(next(RAW_DIR.glob(f"*{key}*.csv")))

    # Trim stray spaces in text columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    # AMFI codes as text
    if "amfi_code" in df.columns:
        df["amfi_code"] = df["amfi_code"].astype(str)

    # Real dates for any column named "date"
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    before = len(df)
    df = df.drop_duplicates()

    df.to_csv(OUT_DIR / out_name, index=False)
    print(f"{out_name}: {before} rows -> {len(df)} rows, "
          f"{df.isnull().sum().sum()} empty cells")