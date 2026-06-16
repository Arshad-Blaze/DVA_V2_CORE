import pandas as pd

from services.batch_processing_service import process_folder


def test_folder_row_count(tmp_path):

    f1 = tmp_path / "a.csv"
    f2 = tmp_path / "b.csv"

    f1.write_text(
        "id,name\n"
        "1,John\n"
    )

    f2.write_text(
        "id,name\n"
        "2,Mary\n"
    )

    output = tmp_path / "output.parquet"

    process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    df = pd.read_parquet(output)

    assert len(df) == 4
