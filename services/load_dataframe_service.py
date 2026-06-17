import pandas as pd


def load_dataframe(path):
    # ✅ Fix: support Path objects
    path = str(path)

    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    elif path.endswith(".csv"):
        return pd.read_csv(path)
    else:
        raise ValueError("Unsupported file format")
