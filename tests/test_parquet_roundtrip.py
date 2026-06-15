import pandas as pd

from services.processing_service import process_file


def test_parquet_round_trip(tmp_path):

    source = tmp_path / "input.csv"

    source.write_text(
        "100,John\n"
        "200,Jane\n"
    )

    target = tmp_path / "output.parquet"

    process_file(
        file_path=str(source),
        output_path=str(target),
        delimiter=","
    )

    df = pd.read_parquet(target)

    assert len(df) == 2

    assert df.iloc[0]["col_0"] == "100"
    assert df.iloc[0]["col_1"] == "John"

    assert df.iloc[1]["col_0"] == "200"
    assert df.iloc[1]["col_1"] == "Jane"
