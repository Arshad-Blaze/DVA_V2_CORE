import streamlit as st
import os

from services.detection_service import detect_file
from services.preview_service import preview_data
from services.processing_service import process_file
from engine.layout_loader import load_layout

st.set_page_config(
    page_title="DVA v2",
    layout="wide"
)

st.title("DVA v2 - File Parser")

# =====================================================
# FILE INPUT
# =====================================================

file_path = st.text_input("Input File Path")

start_line = st.number_input(
    "Data Starts From Line",
    min_value=1,
    value=1
)

# =====================================================
# DETECT
# =====================================================

if file_path and os.path.exists(file_path):

    if st.button("Detect File"):

        result = detect_file(file_path)

        st.session_state["detection"] = result

if "detection" in st.session_state:

    detection = st.session_state["detection"]

    st.subheader("Detection Result")

    st.json(detection)

    file_type = detection["file_type"]

    delimiter = detection["delimiter"]

    record_types = detection["record_types"]

    selected_record_type = None

    if record_types:

        selected_record_type = st.selectbox(
            "Record Type",
            ["ALL"] + record_types
        )

        if selected_record_type == "ALL":
            selected_record_type = None

    # =================================================
    # FIXED WIDTH
    # =================================================

    layout = None

    if file_type == "fixed_width":

        layout_file = st.text_input(
            "Layout CSV Path"
        )

        if layout_file:

            try:

                layout = load_layout(layout_file)

                st.success(
                    f"Loaded {len(layout)} fields"
                )

            except Exception as e:

                st.error(str(e))

    # =================================================
    # DELIMITED
    # =================================================

    else:

        st.success(
            f"Detected delimiter: {delimiter}"
        )

    # =================================================
    # PREVIEW
    # =================================================

    if st.button("Preview Data"):

        try:

            df = preview_data(
                file_path=file_path,
                layout=layout,
                delimiter=delimiter,
                start_line=start_line,
                record_type=selected_record_type
            )

            st.session_state["preview_df"] = df

        except Exception as e:

            st.error(f"Preview failed: {e}")

    if "preview_df" in st.session_state:

        st.subheader("Preview")

        st.dataframe(
            st.session_state["preview_df"],
            use_container_width=True
        )

    # =================================================
    # PROCESS
    # =================================================

    output_path = st.text_input(
        "Output Parquet Path",
        "output/output.parquet"
    )

    if st.button("Process File"):

        try:

            result = process_file(
                file_path=file_path,
                output_path=output_path,
                layout=layout,
                delimiter=delimiter,
                start_line=start_line,
                record_type=selected_record_type
            )

            st.success("Processing Complete")

            st.json(result)

        except Exception as e:

            st.error(f"Processing failed: {e}")

else:

    if file_path:

        st.error("File not found")
