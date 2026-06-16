import pandas as pd

from services.merge_service import process_input


def test_process_single_file(tmp_path):

    file = tmp_path / "sales.csv"

    file.write_text(
        "id,name\n"
        "1,John\n"
    )

    output = tmp_path / "output.parquet"

    result = process_input(
        input_path=str(file),
        output_path=str(output),
        delimiter=","
    )

    assert output.exists()
    assert result["rows"] == 2

def test_process_folder(tmp_path):

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

    result = process_input(
        input_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    df = pd.read_parquet(output)

    assert output.exists()
    assert result["files_processed"] == 2
    assert len(df) == 4
