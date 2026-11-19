from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "Data" / "raw"

for file in sorted(RAW_DIR.glob("*.csv")):
    df = pd.read_csv(file)
    print("=" * 60)
    print("FILE:", file.name)
    print("Rows, Columns:", df.shape)
    print("Column names:", list(df.columns))
    print(df.head(3))