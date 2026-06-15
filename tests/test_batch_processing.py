import pandas as pd

from services.batch_processing_service import process_folder


def test_process_folder(tmp_path):

    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"

    file1.write_text(
        "100,John\n"
        "200,Jane\n"
    )

    file2.write_text(
        "300,Bob\n"
        "400,Alice\n"
    )

    output = tmp_path / "combined.parquet"

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    df = pd.read_parquet(output)

    assert len(df) == 4

    assert result["files_processed"] == 2
    assert result["rows"] == 4

def test_empty_folder(tmp_path):

    output = tmp_path / "output.parquet"

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    assert result["files_processed"] == 0
    assert result["rows"] == 0
