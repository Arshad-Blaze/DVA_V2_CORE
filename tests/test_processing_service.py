import os
import pandas as pd

from services.processing_service import process_file


def test_process_to_parquet(tmp_path):

    source = tmp_path / "sample.csv"

    source.write_text(
        "1,John\n"
        "2,Jane\n"
    )

    target = tmp_path / "output.parquet"

    result = process_file(
        file_path=str(source),
        output_path=str(target),
        delimiter=","
    )

    assert os.path.exists(target)

    df = pd.read_parquet(target)

    assert len(df) == 2

    assert result["rows"] == 2
