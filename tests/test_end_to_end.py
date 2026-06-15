import pandas as pd

from services.detection_service import detect_file
from services.processing_service import process_file


def test_end_to_end_csv(tmp_path):

    source = tmp_path / "input.csv"

    source.write_text(
        "1,John\n"
        "2,Jane\n"
    )

    detection = detect_file(str(source))

    assert detection["file_type"] == "delimited"

    target = tmp_path / "output.parquet"

    process_file(
        file_path=str(source),
        output_path=str(target),
        delimiter=detection["delimiter"]
    )

    df = pd.read_parquet(target)

    assert len(df) == 2
