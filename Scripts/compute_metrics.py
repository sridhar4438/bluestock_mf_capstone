"""Day 4: fund performance metrics from cleaned NAV history."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import linregress

BASE_DIR = Path(__file__).resolve().parents[1]
PROC = BASE_DIR / "Data" / "Processed"

TRADING_DAYS = 252
RF_ANNUAL = 0.065
RF_DAILY = RF_ANNUAL / TRADING_DAYS


def load_nav():
    nav = pd.read_csv(PROC / "clean_nav.csv")
    nav["date"] = pd.to_datetime(nav["date"])
    nav["amfi_code"] = nav["amfi_code"].astype(str)
    return nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)


# Task 1: daily returns
def add_returns(nav):
    nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()
    return nav


# Task 2: CAGR
def cagr_for(g, years):
    n = int(TRADING_DAYS * years)
    if len(g) <= n:
        return np.nan
    start, end = g["nav"].iloc[-n - 1], g["nav"].iloc[-1]
    return ((end / start) ** (1 / years) - 1) * 100


def cagr_since_inception(g):
    n = len(g) - 1
    return ((g["nav"].iloc[-1] / g["nav"].iloc[0]) ** (TRADING_DAYS / n) - 1) * 100


def build_cagr(nav):
    rows = []
    for code, g in nav.groupby("amfi_code"):
        rows.append({
            "amfi_code": code,
            "cagr_1yr_pct": cagr_for(g, 1),
            "cagr_3yr_pct": cagr_for(g, 3),
            "cagr_5yr_pct": cagr_for(g, 5),
            "cagr_since_inception_pct": cagr_since_inception(g),
            "years_of_data": round((len(g) - 1) / TRADING_DAYS, 2),
        })
    return pd.DataFrame(rows)


# Tasks 3 and 4: Sharpe and Sortino
def build_sharpe_sortino(nav):
    rows = []
    for code, g in nav.groupby("amfi_code"):
        ex = g["daily_return"].dropna() - RF_DAILY
        down = ex[ex < 0].std()
        rows.append({
            "amfi_code": code,
            "sharpe": ex.mean() / ex.std() * np.sqrt(TRADING_DAYS),
            "sortino": ex.mean() / down * np.sqrt(TRADING_DAYS) if down > 0 else np.nan,
            "ann_volatility_pct": g["daily_return"].std() * np.sqrt(TRADING_DAYS) * 100,
        })
    return pd.DataFrame(rows)


# Task 5: Alpha and Beta vs Nifty 100
def load_benchmarks():
    b = pd.read_csv(PROC / "clean_benchmarks.csv")
    b["date"] = pd.to_datetime(b["date"])
    return b.pivot(index="date", columns="index_name", values="close_value").sort_index()


def find_nifty100(wide):
    for col in wide.columns:
        key = col.upper().replace(" ", "").replace("_", "")
        if key == "NIFTY100":
            return col
    raise ValueError(f"Could not find Nifty 100. Available: {list(wide.columns)}")


def build_alpha_beta(nav):
    wide = load_benchmarks()
    print("Available indices:", list(wide.columns))
    col = find_nifty100(wide)
    bench_ret = wide[col].pct_change().rename("bench_ret")
    rows = []
    for code, g in nav.groupby("amfi_code"):
        df = (g.set_index("date")["daily_return"].to_frame("fund_ret")
                .join(bench_ret, how="inner").dropna())
        res = linregress(df["bench_ret"], df["fund_ret"])
        rows.append({
            "amfi_code": code,
            "beta": res.slope,
            "alpha_ann_pct": res.intercept * TRADING_DAYS * 100,
            "r_squared": res.rvalue ** 2,
        })
    return pd.DataFrame(rows)


# Task 6: Maximum drawdown
def build_max_drawdown(nav):
    rows = []
    for code, g in nav.groupby("amfi_code"):
        dd = g["nav"] / g["nav"].cummax() - 1
        rows.append({"amfi_code": code, "max_drawdown_pct": dd.min() * 100})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    nav = add_returns(load_nav())
    nav.to_csv(PROC / "returns_computed.csv", index=False)

    cagr = build_cagr(nav)
    cagr.to_csv(PROC / "cagr_report.csv", index=False)

    risk = build_sharpe_sortino(nav)
    risk.to_csv(PROC / "sharpe_sortino.csv", index=False)

    ab = build_alpha_beta(nav)
    ab.to_csv(PROC / "alpha_beta.csv", index=False)
    print("\nALPHA / BETA")
    print(ab.describe().round(2))

    dd = build_max_drawdown(nav)
    dd.to_csv(PROC / "max_drawdown.csv", index=False)
    print("\nMAX DRAWDOWN")
    print(dd.describe().round(2))

    print("\nDone. Files saved in Data/Processed")