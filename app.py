import os
import streamlit as st

from services.detection_service import detect_file
from services.preview_service import preview_data
from engine.layout_loader import load_layout

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

    storelist_path = st.text_input("Store List File")

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
