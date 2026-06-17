import pandas as pd
from services.processing_service import process_file


def test_parquet_round_trip(tmp_path):
    source = tmp_path / "input.csv"

    source.write_text(
        "id,name\n"
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
    assert df.iloc[0]["id"] == 100
    assert df.iloc[0]["name"] == "John"
    assert df.iloc[1]["id"] == 200
    assert df.iloc[1]["name"] == "Jane"