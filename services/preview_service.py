
from engine.parser import parse_file
import pandas


def preview_data(
    file_path,
    layout=None,
    delimiter=None,
    start_line=1,
    record_type=None
):

    df = parse_file(
        file_path=file_path,
        layout=layout,
        delimiter=delimiter,
        start_line=start_line,
        record_type=record_type
    )

    return df.head(5)
