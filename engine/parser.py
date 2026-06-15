
import pandas as pd


def parse_line(line, layout=None, delimiter=None):

    if delimiter:

        parts = line.rstrip("\n").split(delimiter)

        return {
            f"col_{i}": value.strip()
            for i, value in enumerate(parts)
        }

    record = {}

    for col in layout:

        raw = line[col["start"]:col["end"]].strip()

        record[col["name"]] = raw

    return record


def parse_file(
    file_path,
    layout=None,
    delimiter=None,
    start_line=1,
    record_type=None
):

    records = []

    with open(
        file_path,
        encoding="utf-8",
        errors="ignore"
    ) as f:

        lines = f.readlines()

    lines = lines[start_line - 1:]

    for line in lines:

        if not line.strip():
            continue

        if record_type:

            if not line.startswith(record_type):
                continue

        rec = parse_line(
            line,
            layout=layout,
            delimiter=delimiter
        )

        records.append(rec)

    return pd.DataFrame(records)
