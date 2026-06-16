import pandas as pd

from services.load_dataframe_service import (
    load_dataframe
)


def test_load_csv(tmp_path):

    file = tmp_path / "sample.csv"

    file.write_text(
        "Store\n"
        "1001\n"
    )

    df = load_dataframe(
        str(file)
    )

    assert len(df) == 1

    assert "Store" in df.columns
