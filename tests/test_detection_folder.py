# tests/test_detection_folder.py

from services.detection_service import detect_file
import os


def test_detect_folder_uses_first_file(tmp_path):

    file1 = tmp_path / "sample1.csv"
    file2 = tmp_path / "sample2.csv"

    file1.write_text(
        "id,name\n"
        "1,John\n"
    )

    file2.write_text(
        "id,name\n"
        "2,Jane\n"
    )

    first_file = sorted(
        [
            os.path.join(tmp_path, f)
            for f in os.listdir(tmp_path)
        ]
    )[0]

    result = detect_file(first_file)

    assert result["file_type"] == "delimited"
    assert result["delimiter"] == ","
