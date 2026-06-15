
import os


def detect_file(file_path):

    with open(
        file_path,
        encoding="utf-8",
        errors="ignore"
    ) as f:

        sample = [f.readline() for _ in range(20)]

    delimiters = [",", "|", ";", "\t"]

    scores = {}

    for d in delimiters:

        scores[d] = sum(
            line.count(d)
            for line in sample
        )

    best = max(scores, key=scores.get)

    if scores[best] > 0:

        return {
            "file_type": "delimited",
            "delimiter": best,
            "record_types": []
        }

    record_types = sorted(
        list(
            set(
                (
                    "HDR"
                    if line.startswith("HDR")
                    else line[0]
                )
                for line in sample
                if line.strip()
            )
        )
    )

    return {
        "file_type": "fixed_width",
        "delimiter": None,
        "record_types": record_types
    }
