import os
import pandas as pd

from engine.parser import parse_file


def process_folder(
    folder_path,
    output_path,
    layout=None,
    delimiter=None,
    start_line=1,
    record_type=None
):

    dataframes = []

    files_processed = 0

    for filename in sorted(os.listdir(folder_path)):

        full_path = os.path.join(
            folder_path,
            filename
        )

        if not os.path.isfile(full_path):
            continue

        # prevent reading output parquet again
        if full_path == output_path:
            continue

        df = parse_file(
            file_path=full_path,
            layout=layout,
            delimiter=delimiter,
            start_line=start_line,
            record_type=record_type
        )

        if not df.empty:
            dataframes.append(df)

        files_processed += 1

    if dataframes:

        combined_df = pd.concat(
            dataframes,
            ignore_index=True
        )

    else:

        combined_df = pd.DataFrame()

    combined_df.to_parquet(
        output_path,
        index=False
    )

    return {
        "files_processed": files_processed,
        "rows": len(combined_df),
        "output": output_path
    }
