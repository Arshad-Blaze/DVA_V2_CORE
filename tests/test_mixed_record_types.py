from engine.parser import parse_file


def test_only_u_records_returned(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "HDRHEADER\n"
        "S12345\n"
        "U11111APPLE\n"
        "U22222BANANA\n"
    )

    layout = [
        {
            "name": "raw",
            "start": 0,
            "end": 50
        }
    ]

    df = parse_file(
        str(file),
        layout=layout,
        record_type="U"
    )

    assert len(df) == 2

    assert "APPLE" in df.iloc[0]["raw"]
    assert "BANANA" in df.iloc[1]["raw"]
