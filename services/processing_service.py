import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def _read_csv_smart(file_path, delimiter, chunksize, skiprows=0, record_type=None):
    import pandas as pd

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Apply skiprows
    lines = lines[skiprows:]

    # ✅ Apply record_type filter at LINE level
    if record_type:
        lines = [l for l in lines if l.startswith(record_type)]

    # ✅ If no lines left → return empty iterator
    if not lines:
        yield pd.DataFrame()
        return

    # ✅ Normalize column length (important fix)
    split_lines = [l.strip().split(delimiter) for l in lines]
    max_cols = max(len(row) for row in split_lines)

    normalized = [
        row + [""] * (max_cols - len(row))
        for row in split_lines
    ]

    
    df = pd.DataFrame(normalized)

    # ✅ Detect header row (simple rule)
    first_row = df.iloc[0].astype(str).tolist()

    is_header = all(not x.isdigit() for x in first_row)

    # ✅ Only drop header if NO record_type filtering
    # (because U records don't have headers)
    if is_header and record_type is None:
        df = df.iloc[1:].reset_index(drop=True)


    # ✅ yield in chunks
    for i in range(0, len(df), chunksize):
        yield df.iloc[i:i+chunksize]

def process_file(
    file_path,
    output_path,
    layout=None,
    delimiter=",",
    start_line=1,
    record_type=None,
    chunksize=100_000
):
    writer = None
    total_rows = 0

    for chunk in _read_csv_smart(
        file_path,
        delimiter=delimiter,
        chunksize=chunksize,
        skiprows=start_line - 1,
        record_type=record_type
    ):

        total_rows += len(chunk)

        table = pa.Table.from_pandas(chunk)

        if writer is None:
            writer = pq.ParquetWriter(output_path, table.schema)

        writer.write_table(table)

    if writer:
        writer.close()

    return {
        "rows": total_rows,
        "output": output_path
    }