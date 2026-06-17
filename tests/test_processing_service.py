import pandas as pd
from services.batch_processing_service import process_folder


def test_process_folder_basic(tmp_path):
    folder = tmp_path / "data"
    folder.mkdir()

    (folder / "a.csv").write_text("id,name\n1,John\n")
    (folder / "b.csv").write_text("id,name\n2,Mary\n")

    output_file = tmp_path / "merged.parquet"

    result = process_folder(
        folder_path=str(folder),
        output_path=str(output_file),
        delimiter=","
    )

    df = pd.read_parquet(output_file)

    assert output_file.exists()
    assert result["files_processed"] == 2
    assert len(df) == 2

def test_process_file_record_type_filter(tmp_path):
    from services.processing_service import process_file
    import pandas as pd

    file = tmp_path / "input.txt"

    file.write_text(
        "HDR,header\n"
        "S,summary\n"
        "U,1,John\n"
        "U,2,Mary\n"
    )

    output = tmp_path / "out.parquet"

    result = process_file(
        file_path=str(file),
        output_path=str(output),
        delimiter=",",
        record_type="U"
    )

    df = pd.read_parquet(output)

    assert len(df) == 2
    assert all(df.iloc[:, 0] == "U")

def test_process_file_no_record_filter(tmp_path):
    from services.processing_service import process_file
    import pandas as pd

    file = tmp_path / "input.txt"

    file.write_text(
        "HDR,header\n"
        "U,1,John\n"
    )

    output = tmp_path / "out.parquet"

    process_file(
        file_path=str(file),
        output_path=str(output),
        delimiter=","
    )

    df = pd.read_parquet(output)

    assert len(df) == 2   # all rows preserved