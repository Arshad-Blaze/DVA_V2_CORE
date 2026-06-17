import pandas as pd
from services.batch_processing_service import process_folder


def test_process_folder_creates_parquet(tmp_path):
    file1 = tmp_path / "a.csv"

    file1.write_text(
        "id,name\n"
        "1,John\n"
    )

    output = tmp_path / "output.parquet"

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    assert output.exists()

    df = pd.read_parquet(output)

    assert len(df) == 1
    assert result["files_processed"] == 1