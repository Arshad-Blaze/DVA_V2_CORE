from services.preview_service import preview_data


def test_preview_row_limit(tmp_path):

    file = tmp_path / "sample.csv"

    file.write_text(
        "1,John\n"
        "2,Mary\n"
        "3,Alex\n"
        "4,Bob\n"
        "5,Jane\n"
    )

    df = preview_data(
        file_path=str(file),
        delimiter=",",
        max_rows=2
    )

    assert len(df) == 2
