from engine.parser import parse_file


def test_parse_delimited(tmp_path):

    file = tmp_path / "sample.csv"

    file.write_text(
        "1,John\n"
        "2,Jane\n"
    )

    df = parse_file(
        str(file),
        delimiter=","
    )

    assert len(df) == 2

    assert df.iloc[0]["col_0"] == "1"
    assert df.iloc[0]["col_1"] == "John"


def test_parse_fixed_width(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "12345John      \n"
        "54321Jane      \n"
    )

    layout = [
        {
            "name": "id",
            "start": 0,
            "end": 5
        },
        {
            "name": "name",
            "start": 5,
            "end": 15
        }
    ]

    df = parse_file(
        str(file),
        layout=layout
    )

    assert len(df) == 2

    assert df.iloc[0]["id"] == "12345"
    assert df.iloc[0]["name"] == "John"


def test_record_type_filter(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "HDRHEADER\n"
        "U12345APPLE\n"
        "U54321BANANA\n"
    )

    layout = [
        {
            "name": "raw",
            "start": 0,
            "end": 20
        }
    ]

    df = parse_file(
        str(file),
        layout=layout,
        record_type="U"
    )

    assert len(df) == 2
