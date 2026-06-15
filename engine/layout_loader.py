
import pandas as pd


def load_layout(layout_file):

    df = pd.read_csv(layout_file)

    df.columns = df.columns.str.strip().str.lower()

    layout = []

    for _, row in df.iterrows():

        start = int(row["from"]) - 1
        length = int(row["length"])

        layout.append({
            "name": row["field"],
            "start": start,
            "end": start + length,
            "type": str(row.get("type", "text")).lower()
        })

    return layout
