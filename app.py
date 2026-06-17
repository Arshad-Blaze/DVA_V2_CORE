import os
import streamlit as st
import pandas as pd
import tempfile
import logging
import time

from engine.layout_loader import load_layout

from services.detection_service import detect_file
from services.preview_service import preview_data
from services.merge_service import process_input
from services.load_dataframe_service import load_dataframe
from services.storelist_service import compare_storelist
from services.validation_service import validate_stores_auto
from services.report_service import generate_excel_report
from services.config_service import load_config, save_config
from services.batch_processing_service import process_folder

# =====================================================
# LOGGING CONFIG
# =====================================================

logging.basicConfig(
    filename="dva_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_step(step):
    logging.info(f"STEP: {step}")

def timed_step(label):
    start = time.time()
    st.info(f"{label} started...")
    log_step(label)
    return start

def end_timed_step(label, start):
    duration = round(time.time() - start, 2)
    st.success(f"{label} completed in {duration} sec ✅")
    logging.info(f"{label} took {duration} seconds")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="DVA Tool", layout="wide")

st.title("DVA Tool")

# =====================================================
# SIDEBAR STATUS
# =====================================================

st.sidebar.header("System Status")
st.sidebar.write("✔ Detection Ready")
st.sidebar.write("✔ Validation Ready")
st.sidebar.write("✔ Reporting Ready")

# =====================================================
# SESSION STATE
# =====================================================

for key in [
    "detection_result",
    "preview_df",
    "process_df",
    "storelist_df",
    "storelist_result"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# =====================================================
# TABS (NEW)
# =====================================================

tab1, tab2 = st.tabs(["Onboarding", "Validation"])

# =====================================================
# ONBOARDING TAB
# =====================================================

with tab1:

    st.header("Onboarding")

    input_type = st.radio("Retailer Input", ["File", "Folder"])
    input_path = st.text_input("Retailer Path")

    if st.button("Detect"):

        if not input_path:
            st.error("Provide a path")
            st.stop()

        if os.path.isfile(input_path):
            result = detect_file(input_path)

        elif os.path.isdir(input_path):
            files = [
                os.path.join(input_path, f)
                for f in os.listdir(input_path)
                if os.path.isfile(os.path.join(input_path, f))
            ]
            if not files:
                st.error("Folder empty")
                st.stop()

            result = detect_file(files[0])

        else:
            st.error("Invalid path")
            st.stop()

        st.session_state["detection_result"] = result

    # Detection results
    if st.session_state["detection_result"]:

        result = st.session_state["detection_result"]

        st.subheader("Detection Results")
        st.write("File Type:", result.get("file_type"))
        st.write("Delimiter:", result.get("delimiter"))

        for line in result.get("sample_lines", []):
            st.code(line)

        preview_rows = st.number_input("Preview Rows", 1, 100, 20)

        if st.button("Preview"):

            df = preview_data(
                file_path=input_path,
                delimiter=result.get("delimiter"),
                max_rows=preview_rows
            )

            st.session_state["preview_df"] = df

    # Preview display
    if st.session_state["preview_df"] is not None:
        st.dataframe(st.session_state["preview_df"])

    # Processing
    if st.session_state["preview_df"] is not None:

        output_path = st.text_input("Output Parquet Path", "output.parquet")

        if st.button("Process"):

            start = timed_step("Processing")

            process_input(
                input_path=input_path,
                output_path=output_path,
                delimiter=result.get("delimiter")
            )

            end_timed_step("Processing", start)

            st.session_state["process_df"] = pd.read_parquet(output_path).head(100)

    if st.session_state["process_df"] is not None:
        st.dataframe(st.session_state["process_df"])

# =====================================================
# VALIDATION TAB
# =====================================================

with tab2:

    st.header("Validation")

    bau_path = st.text_input("BAU Path")
    test_path = st.text_input("TEST Path")

    # ✅ Config and toggles
    st.subheader("Options")

    units_implied = st.checkbox("Units Implied (/100)")
    dollars_implied = st.checkbox("Sales Implied (/100)")
    unit_price_implied = st.checkbox("Unit Price Implied (/100)")

    use_config = st.checkbox("Use Config File")
    config = {
        "units_implied": units_implied,
        "dollars_implied": dollars_implied,
        "unit_price_implied": unit_price_implied
    }

    if use_config:
        config_path = st.text_input("Config Path")

        if config_path:
            if os.path.exists(config_path):
                saved = load_config(config_path)
                saved.update(config)
                config = saved
                st.success("Config Loaded ✅")
            else:
                st.error("Invalid config path")

    save_config_toggle = st.checkbox("Save Config After Run")

    # ✅ Validation
    if st.button("Run Validation"):
              
        if os.path.isdir(bau_path):
            st.info("Processing BAU folder...")
            bau_temp = "bau_merged.parquet"
            process_folder(bau_path, bau_temp)
            bau_path = bau_temp

        if os.path.isdir(test_path):
            st.info("Processing TEST folder...")
            test_temp = "test_merged.parquet"
            process_folder(test_path, test_temp)
            test_path = test_temp


        start = timed_step("Validation")

        result = validate_stores_auto(
            bau_path,
            test_path,
            config=config
        )

        end_timed_step("Validation", start)

        # ✅ SUMMARY TABLE
        st.subheader("Validation Summary")

        summary_df = pd.DataFrame([result["summary"]])
        st.dataframe(summary_df, use_container_width=True)

        # ✅ KPI METRICS
        st.subheader("Key Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Units Diff", result["summary"]["units_diff"])
        col2.metric("Sales Diff", result["summary"]["dollars_diff"])
        col3.metric(
            "Units %",
            f"{result['summary']['units_pct']*100:.2f}%"
        )

        # ✅ Mapping view
        st.subheader("Mapping Info")

        if "mapping" in config:
            st.json(config["mapping"])
        else:
            st.info("Auto mapping used")

        # ✅ Store preview
        st.subheader("Store Validation Preview")

        st.dataframe(
            pd.DataFrame(result["store_report"]).head(50),
            use_container_width=True
        )

        # ✅ Excel download
        report_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")

        generate_excel_report(result, report_file.name)

        with open(report_file.name, "rb") as f:
            st.download_button(
                "Download Excel Report",
                data=f,
                file_name="validation_report.xlsx"
            )

        # ✅ Save config
        if save_config_toggle:

            config_file = st.text_input("Save Config Path", "config.json")

            if config_file:
                save_config(config, config_file)
                st.success("Config Saved ✅")