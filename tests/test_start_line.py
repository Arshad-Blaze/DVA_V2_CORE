from engine.parser import parse_file


def test_start_line(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "HEADER\n"
        "IGNORE\n"
        "100,John\n"
        "200,Jane\n"
    )

    df = parse_file(
        str(file),
        delimiter=",",
        start_line=3
    )

    assert len(df) == 2

    assert df.iloc[0]["col_0"] == "100"
    assert df.iloc[1]["col_0"] == "200"
