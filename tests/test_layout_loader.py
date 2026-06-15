from engine.layout_loader import load_layout


def test_load_layout(tmp_path):

    layout = tmp_path / "layout.csv"

    layout.write_text(
        "Field,From,Length,Type\n"
        "id,1,5,text\n"
        "name,6,10,text\n"
    )

    result = load_layout(str(layout))

    assert len(result) == 2

    assert result[0]["name"] == "id"
    assert result[0]["start"] == 0
    assert result[0]["end"] == 5

    assert result[1]["name"] == "name"
