from engine.parser import parse_file


def test_empty_file(tmp_path):

    file = tmp_path / "empty.txt"

    file.write_text("")

    df = parse_file(str(file))

    assert len(df) == 0
