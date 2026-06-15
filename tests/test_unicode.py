from engine.parser import parse_file


def test_unicode_characters(tmp_path):

    file = tmp_path / "unicode.csv"

    file.write_text(
        "1,محمد\n"
        "2,Français\n"
        "3,Español\n",
        encoding="utf-8"
    )

    df = parse_file(
        str(file),
        delimiter=","
    )

    assert len(df) == 3

    assert df.iloc[0]["col_1"] == "محمد"
    assert df.iloc[1]["col_1"] == "Français"
    assert df.iloc[2]["col_1"] == "Español"
