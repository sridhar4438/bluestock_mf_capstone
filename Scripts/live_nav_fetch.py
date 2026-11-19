import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "Data" / "raw"

def fetch_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    df = pd.DataFrame(payload["data"])
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = df["nav"].astype(float)
    df["amfi_code"] = scheme_code
    df["scheme_name"] = payload["meta"]["scheme_name"]
    return df.sort_values("date")

codes = ["125497", "119551", "120503", "118632", "119092", "120841"]

for code in codes:
    df = fetch_nav(code)
    df.to_csv(RAW_DIR / f"live_nav_{code}.csv", index=False)
    print(code, "->", len(df), "rows saved")