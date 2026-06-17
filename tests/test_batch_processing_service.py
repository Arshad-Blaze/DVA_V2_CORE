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

def test_process_folder_basic(tmp_path):
    import pandas as pd
    from services.batch_processing_service import process_folder

    folder = tmp_path / "data"
    folder.mkdir()

    df1 = pd.DataFrame({"store": [1], "units": [10]})
    df2 = pd.DataFrame({"store": [2], "units": [20]})

    df1.to_csv(folder / "file1.csv", index=False)
    df2.to_csv(folder / "file2.csv", index=False)

    output_file = tmp_path / "merged.parquet"

    result = process_folder(str(folder), str(output_file))

    df_out = pd.read_parquet(output_file)

    assert len(df_out) == 2
    assert result["files_processed"] == 2

def test_process_folder_ignore_files(tmp_path):
    import pandas as pd
    from services.batch_processing_service import process_folder

    folder = tmp_path / "data"
    folder.mkdir()

    df = pd.DataFrame({"store": [1], "units": [10]})
    df.to_csv(folder / "file.csv", index=False)

    # unsupported file
    with open(folder / "readme.txtx", "w") as f:
        f.write("ignore me")

    output_file = tmp_path / "merged.parquet"

    result = process_folder(str(folder), str(output_file))

    assert result["files_processed"] == 1

def test_process_folder_empty(tmp_path):
    from services.batch_processing_service import process_folder

    folder = tmp_path / "empty"
    folder.mkdir()

    output_file = tmp_path / "out.parquet"

    result = process_folder(str(folder), str(output_file))

    assert result["files_processed"] == 0

def test_process_folder_record_type_filter(tmp_path):
    import pandas as pd
    from services.batch_processing_service import process_folder

    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"

    f1.write_text(
        "HDR,header\n"
        "U,1\n"
    )

    f2.write_text(
        "S,skip\n"
        "U,2\n"
    )

    output = tmp_path / "out.parquet"

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=",",
        record_type="U"
    )

    df = pd.read_parquet(output)

    assert len(df) == 2

def test_record_filter_no_matches(tmp_path):
    from services.processing_service import process_file
    import pandas as pd

    file = tmp_path / "input.txt"

    file.write_text(
        "HDR,header\n"
        "S,summary\n"
    )

    output = tmp_path / "out.parquet"

    process_file(
        file_path=str(file),
        output_path=str(output),
        delimiter=",",
        record_type="U"
    )

    df = pd.read_parquet(output)

    assert len(df) == 0

