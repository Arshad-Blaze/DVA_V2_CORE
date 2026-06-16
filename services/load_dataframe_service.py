import pandas as pd


def load_dataframe(path):

    if path.endswith(".parquet"):
        return pd.read_parquet(path)

    return pd.read_csv(
        path,
        dtype=str
    )
