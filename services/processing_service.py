
import os

from engine.parser import parse_file


def process_file(
    file_path,
    output_path,
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

    df.to_parquet(
        output_path,
        index=False
    )

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "output": output_path
    }
