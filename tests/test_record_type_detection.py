from services.detection_service import detect_file


def test_detect_record_types(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "HDRHEADER\n"
        "S12345\n"
        "U11111APPLE\n"
        "U22222BANANA\n"
    )

    result = detect_file(str(file))

    assert "HDR" in result["record_types"]
    assert "S" in result["record_types"]
    assert "U" in result["record_types"]
