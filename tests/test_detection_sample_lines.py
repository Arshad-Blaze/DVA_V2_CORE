from services.detection_service import detect_file

def test_sample_lines_returned(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "A\n"
        "B\n"
        "C\n"
        "D\n"
    )

    result = detect_file(str(file))

    assert "sample_lines" in result
    assert len(result["sample_lines"]) > 0
