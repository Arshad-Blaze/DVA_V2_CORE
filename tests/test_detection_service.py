from services.detection_service import detect_file


def test_detect_csv(tmp_path):

    file = tmp_path / "sample.csv"

    file.write_text(
        "id,name\n"
        "1,John\n"
        "2,Jane\n"
    )

    result = detect_file(str(file))

    assert result["file_type"] == "delimited"
    assert result["delimiter"] == ","


def test_detect_pipe(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "1|John\n"
        "2|Jane\n"
    )

    result = detect_file(str(file))

    assert result["file_type"] == "delimited"
    assert result["delimiter"] == "|"


def test_detect_fixed_width(tmp_path):

    file = tmp_path / "fixed.txt"

    file.write_text(
        "12345John     \n"
        "54321Jane     \n"
    )

    result = detect_file(str(file))

    assert result["file_type"] == "fixed_width"
