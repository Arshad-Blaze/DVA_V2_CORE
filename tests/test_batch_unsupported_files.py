# tests/test_batch_unsupported_files.py

from services.batch_processing_service import process_folder


def test_batch_ignores_non_data_files(tmp_path):

    data_file = tmp_path / "data.csv"
    data_file.write_text(
        "id,name\n"
        "1,John\n"
    )

    log_file = tmp_path / "process.log"
    log_file.write_text("log content")

    tmp_file = tmp_path / "temp.tmp"
    tmp_file.write_text("temporary")

    output = tmp_path / "output.parquet"

    result = process_folder(
        folder_path=str(tmp_path),
        output_path=str(output),
        delimiter=","
    )

    # For now this may fail.
    # If it fails we'll harden batch_processing_service.
    assert result["files_processed"] == 1
