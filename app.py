import os
import streamlit as st
import pandas as pd


from engine.layout_loader import load_layout

from services.detection_service import detect_file
from services.preview_service import preview_data
from services.processing_service import process_file
from services.batch_processing_service import process_folder
from services.merge_service import process_input
from services.load_dataframe_service import load_dataframe
from services.storelist_service import compare_storelist

st.set_page_config(
    page_title="DVA Tool",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "detection_result" not in st.session_state:
    st.session_state["detection_result"] = None

if "preview_df" not in st.session_state:
    st.session_state["preview_df"] = None

if "process_df" not in st.session_state:
    st.session_state["process_df"] = None

if "storelist_df" not in st.session_state:
    st.session_state["storelist_df"] = None

if "storelist_result" not in st.session_state:
    st.session_state["storelist_result"] = None

# =====================================================
# UI
# =====================================================

st.title("DVA Tool")

workflow = st.radio(
    "Select Workflow",
    [
        "Onboarding",
        "Existing"
    ]
)

input_path = None
layout = None

# =====================================================
# ONBOARDING
# =====================================================

if workflow == "Onboarding":

    st.header("Onboarding")

    retailer_input_type = st.radio(
        "Retailer Input",
        [
            "File",
            "Folder"
        ]
    )


    if retailer_input_type == "File":
        retailer_path = st.text_input("Retailer File")
    else:
        retailer_path = st.text_input("Retailer Folder")

    input_path = retailer_path

    if st.button("Detect", key="onboarding_detect"):

        if not input_path:
            st.error("Please provide a file or folder path")
            st.stop()

        if os.path.isfile(input_path):

            result = detect_file(input_path)

        elif os.path.isdir(input_path):

            files = sorted([
                os.path.join(input_path, f)
                for f in os.listdir(input_path)
                if os.path.isfile(os.path.join(input_path, f))
            ])

            if not files:
                st.error("Folder is empty")
                st.stop()

            result = detect_file(files[0])

        else:
            st.error("Invalid path")
            st.stop()

        st.session_state["detection_result"] = result

# =====================================================
# EXISTING
# =====================================================

else:

    st.header("Existing")

    bau_path = st.text_input("BAU File / Folder")

    test_path = st.text_input("TEST File / Folder")

    input_path = bau_path

    if st.button("Detect", key="existing_detect"):

        if not bau_path:
            st.error("Please provide BAU path")
            st.stop()

        if os.path.isfile(bau_path):

            result = detect_file(bau_path)

        elif os.path.isdir(bau_path):

            files = sorted([
                os.path.join(bau_path, f)
                for f in os.listdir(bau_path)
                if os.path.isfile(os.path.join(bau_path, f))
            ])

            if not files:
                st.error("Folder is empty")
                st.stop()

            result = detect_file(files[0])

        else:
            st.error("Invalid BAU path")
            st.stop()

        st.session_state["detection_result"] = result

# =====================================================
# DETECTION RESULTS
# =====================================================

if st.session_state["detection_result"]:

    result = st.session_state["detection_result"]

    st.subheader("Detection Results")

    st.write(
        "File Type:",
        result.get("file_type")
    )

    st.write(
        "Delimiter:",
        result.get("delimiter")
    )

    st.write("Record Types:")

    for r in result.get("record_types", []):
        st.write(f"- {r}")

    st.subheader("Sample Lines")

    for line in result.get("sample_lines", []):
        st.code(line)

    # =================================================
    # PREVIEW
    # =================================================

    preview_rows = st.number_input(
        "Preview Rows",
        min_value=1,
        max_value=100,
        value=20
    )
    has_header = st.checkbox(
    "First row contains headers",
    value=True
    )

    if result["file_type"] == "delimited":

        if st.button("Preview"):

            try:

                df = preview_data(
                    file_path=input_path,
                    delimiter=result["delimiter"],
                    max_rows=preview_rows
                )

                st.session_state["preview_df"] = df

            except Exception as e:

                st.error(
                    f"Preview failed: {e}"
                )

    else:

        layout_file = st.text_input(
            "Layout CSV File"
        )

        if st.button("Preview Fixed Width"):

            try:

                layout = load_layout(
                    layout_file
                )

                df = preview_data(
                    file_path=input_path,
                    layout=layout,
                    max_rows=preview_rows
                )

                st.session_state["preview_df"] = df

            except Exception as e:

                st.error(
                    f"Preview failed: {e}"
                )

# =====================================================
# PREVIEW DISPLAY
# =====================================================

if st.session_state["preview_df"] is not None:

    st.subheader("Parsed Preview")

    st.dataframe(
        st.session_state["preview_df"],
        use_container_width=True
    )

# =====================================================
# PROCESS
# =====================================================

if st.session_state["preview_df"] is not None:

    st.subheader("Process")

    output_path = st.text_input(
        "Output Parquet Path",
        "output.parquet"
    )

    if st.button("Process"):

        detection = st.session_state["detection_result"]

        try:
            result = process_input(
            input_path=input_path,
            output_path=output_path,
            layout=layout,
            delimiter=detection.get("delimiter")
        )
            st.success("Processing Complete")

            st.json(result)

        except Exception as e:

            st.error(
                f"Processing failed: {e}"
            )


        process_df = pd.read_parquet(output_path).head(100)

        st.session_state["process_df"] = process_df

    if st.session_state["process_df"] is not None:

        st.subheader("Processed Data")

        st.dataframe(
            st.session_state["process_df"],
            use_container_width=True
        )
# =====================================================
# STORE LIST COMPARISON
# =====================================================

if workflow == "Onboarding":

    st.subheader("Store List Comparison")

    storelist_path = st.text_input(
        "Store List File"
    )

    if storelist_path:

        try:

            storelist_df = load_dataframe(
                storelist_path
            )

            st.session_state[
                "storelist_df"
            ] = storelist_df

            st.dataframe(
                storelist_df.head()
            )

        except Exception as e:

            st.error(
                f"Store list load failed: {e}"
            )
if (
    workflow == "Onboarding"
    and st.session_state["process_df"] is not None
    and st.session_state["storelist_df"] is not None
):

    retailer_df = st.session_state["process_df"]

    storelist_df = st.session_state["storelist_df"]

    retailer_store_col = st.selectbox(
        "Retailer Store Column",
        retailer_df.columns
    )

    storelist_col = st.selectbox(
        "Store List Column",
        storelist_df.columns
    )

    if st.button("Compare Store List"):

        result = compare_storelist(
            retailer_df=retailer_df,
            storelist_df=storelist_df,
            retailer_store_column=retailer_store_col,
            storelist_column=storelist_col
        )

        st.session_state["storelist_result"] = result
if st.session_state["storelist_result"]:

    st.subheader(
        "Store List Results"
    )

    st.json(
        st.session_state[
            "storelist_result"
        ]
    )
