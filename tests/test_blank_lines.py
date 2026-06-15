from engine.parser import parse_file


def test_blank_lines_are_skipped(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "100,John\n"
        "\n"
        "\n"
        "200,Jane\n"
        "\n"
    )

    df = parse_file(
        str(file),
        delimiter=","
    )

    assert len(df) == 2

    assert df.iloc[0]["col_0"] == "100"
    assert df.iloc[1]["col_0"] == "200"
