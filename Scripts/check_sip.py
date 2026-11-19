from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parent.parent / "Data" / "processed" / "clean_sip_inflows.csv"
df = pd.read_csv(path)

print(df.isnull().sum()[df.isnull().sum() > 0])
print()
print(df[df.isnull().any(axis=1)].head(15))