# tests/test_batch_ignores_output.py

import pandas as pd
from services.batch_processing_service import process_folder


def test_output_file_not_counted(tmp_path):

    file1 = tmp_path / "file1.csv"

    file1.write_text(
        "id,name\n"
        "1,John\n"
    )

    output = tmp_path / "output.parquet"

    # Existing parquet already in folder
    pd.DataFrame(
        {"dummy": [1]}
    ).to_parquet(output)

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    # Only CSV should be processed
    assert result["files_processed"] == 1

    # Output parquet should contain processed data
    df = pd.read_parquet(output)

    assert not df.empty

    # ✅ FIX: only actual data rows (header excluded)
    assert len(df) == 1

    # ✅ FIX: use real column names
    assert df.iloc[0]["id"] == 1
    assert df.iloc[0]["name"] == "John"