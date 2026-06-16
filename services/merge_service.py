import os

from services.processing_service import process_file
from services.batch_processing_service import process_folder


def process_input(
    input_path,
    output_path,
    layout=None,
    delimiter=None,
    start_line=1,
    record_type=None
):

    if os.path.isfile(input_path):

        return process_file(
            file_path=input_path,
            output_path=output_path,
            layout=layout,
            delimiter=delimiter,
            start_line=start_line,
            record_type=record_type
        )

    elif os.path.isdir(input_path):

        return process_folder(
            folder_path=input_path,
            output_path=output_path,
            layout=layout,
            delimiter=delimiter,
            start_line=start_line,
            record_type=record_type
        )

    raise ValueError(
        f"Invalid input path: {input_path}"
    )
