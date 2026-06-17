
import pandas as pd
from services.report_service import generate_excel_report

def test_excel_file_created(tmp_path):

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {"bau_units": 100, "test_units": 90, "units_diff": 10, "units_pct": 0.1,
                    "bau_dollars": 1000, "test_dollars": 900, "dollars_diff": 100, "dollars_pct": 0.1},
        "store_report": [],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    assert output_file.exists()

def test_excel_sheet_names(tmp_path):

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {"bau_units": 1, "test_units": 1, "units_diff": 0, "units_pct": 0,
                    "bau_dollars": 1, "test_dollars": 1, "dollars_diff": 0, "dollars_pct": 0},
        "store_report": [],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    xl = pd.ExcelFile(output_file)

    expected_sheets = {
        "Summary",
        "Store Validation",
        "UPC Validation",
        "Missing Stores",
        "Extra Stores"
    }

    assert expected_sheets.issubset(set(xl.sheet_names))

def test_summary_sheet_content(tmp_path):

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {
            "bau_units": 100,
            "test_units": 90,
            "units_diff": 10,
            "units_pct": 0.1,
            "bau_dollars": 1000,
            "test_dollars": 900,
            "dollars_diff": 100,
            "dollars_pct": 0.1
        },
        "store_report": [],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Summary")

    assert "bau_units" in df.columns
    assert df.iloc[0]["bau_units"] == 100

def test_store_sheet_data(tmp_path):

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {},
        "store_report": [
            {"store": 1, "bau_units": 10, "test_units": 8,
             "units_diff": 2, "units_pct": 0.2,
             "bau_dollars": 100, "test_dollars": 80,
             "dollars_diff": 20, "dollars_pct": 0.2}
        ],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Store Validation")

    assert len(df) == 1
    assert df.iloc[0]["store"] == 1

def test_missing_stores_sheet(tmp_path):

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {},
        "store_report": [],
        "missing_stores": [1, 2],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Missing Stores")

    assert set(df.iloc[:, 0]) == {1, 2}

def test_percentage_converted_to_100_scale(tmp_path):
    import pandas as pd
    from services.report_service import generate_excel_report

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {
            "bau_units": 100,
            "test_units": 90,
            "units_diff": 10,
            "units_pct": 0.1,
            "bau_dollars": 1000,
            "test_dollars": 900,
            "dollars_diff": 100,
            "dollars_pct": 0.1
        },
        "store_report": [],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Summary")

    # ✅ expect 0.1 → 10
    assert df.iloc[0]["units_pct"] == 10

def test_percentage_rounding(tmp_path):
    import pandas as pd
    from services.report_service import generate_excel_report

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {
            "bau_units": 100,
            "test_units": 90,
            "units_diff": 10,
            "units_pct": 0.123456,
            "bau_dollars": 1000,
            "test_dollars": 900,
            "dollars_diff": 100,
            "dollars_pct": 0.123456
        },
        "store_report": [],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Summary")

    # ✅ rounded to 2 decimal places
    assert round(df.iloc[0]["units_pct"], 2) == 12.35

def test_store_sheet_percentage_scaled(tmp_path):
    import pandas as pd
    from services.report_service import generate_excel_report

    output_file = tmp_path / "report.xlsx"

    mock_result = {
        "summary": {},
        "store_report": [
            {
                "store": 1,
                "bau_units": 100,
                "test_units": 90,
                "units_diff": 10,
                "units_pct": 0.1,
                "bau_dollars": 1000,
                "test_dollars": 900,
                "dollars_diff": 100,
                "dollars_pct": 0.1
            }
        ],
        "missing_stores": [],
        "extra_stores": [],
        "upc_report": []
    }

    generate_excel_report(mock_result, output_file)

    df = pd.read_excel(output_file, sheet_name="Store Validation")

    assert df.iloc[0]["units_pct"] == 10

