from services.preview_service import preview_data


def test_preview_returns_dataframe(tmp_path):

    file = tmp_path / "sample.csv"

    file.write_text(
        "1,John\n"
        "2,Jane\n"
    )

    df = preview_data(
        str(file),
        delimiter=","
    )

    assert len(df) == 2
