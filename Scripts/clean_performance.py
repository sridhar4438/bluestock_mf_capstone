from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data" / "raw"
OUT_DIR = BASE_DIR / "Data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

perf = pd.read_csv(next(RAW_DIR.glob("*scheme_performance*.csv")))
master = pd.read_csv(next(RAW_DIR.glob("*fund_master*.csv")))

perf["amfi_code"] = perf["amfi_code"].astype(str)

# 1. Make sure number columns are real numbers
number_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
               "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
               "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct"]
for col in number_cols:
    if col in perf.columns:
        perf[col] = pd.to_numeric(perf[col], errors="coerce")

print("Rows:", len(perf))
print("Empty cells:")
print(perf.isnull().sum()[perf.isnull().sum() > 0])
print("(nothing listed above means no empty cells)")
print()

# 2. Flag negative Sharpe ratios
perf["negative_sharpe_flag"] = perf["sharpe_ratio"] < 0
print("Funds with negative Sharpe:", perf["negative_sharpe_flag"].sum())
print()

# 3. Check expense ratio range in fund master
bad_exp = master[(master["expense_ratio_pct"] < 0.1) | (master["expense_ratio_pct"] > 2.5)]
print("Expense ratio outside 0.1% - 2.5%:", len(bad_exp))
if len(bad_exp) > 0:
    print(bad_exp[["amfi_code", "scheme_name", "expense_ratio_pct"]])
print()

perf.to_csv(OUT_DIR / "clean_performance.csv", index=False)
print("Saved to Data/processed/clean_performance.csv")