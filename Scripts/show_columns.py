from pathlib import Path
import pandas as pd

PROC_DIR = Path(__file__).resolve().parent.parent / "Data" / "processed"

for file in sorted(PROC_DIR.glob("clean_*.csv")):
    df = pd.read_csv(file, nrows=2)
    print(file.name)
    print(list(df.columns))
    print()