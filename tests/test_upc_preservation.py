from engine.parser import parse_file


def test_large_upc_preserved_as_string(tmp_path):

    file = tmp_path / "upc.txt"

    file.write_text(
        "000060810195550371,APPLE\n"
    )

    df = parse_file(
        str(file),
        delimiter=","
    )

    assert len(df) == 1

    assert df.iloc[0]["col_0"] == "000060810195550371"

    assert isinstance(
        df.iloc[0]["col_0"],
        str
    )
