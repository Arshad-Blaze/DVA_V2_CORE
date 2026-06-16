from services.preview_service import preview_data
from engine.layout_loader import load_layout


def test_fixed_width_preview(tmp_path):

    layout = tmp_path / "layout.csv"

    layout.write_text(
        "field,from,length,type\n"
        "store,1,4,text\n"
        "upc,5,12,text\n"
    )

    data = tmp_path / "sample.txt"

    data.write_text(
        "1001123456789012\n"
    )

    df = preview_data(
        file_path=str(data),
        layout=load_layout(str(layout))
    )

    assert df.iloc[0]["store"] == "1001"
