import pandas as pd


def _convert_pct_columns(df):
    """
    Convert percentage columns from fraction (0.1) to percentage (10.0)
    and round to 2 decimals.
    """
    for col in ["units_pct", "dollars_pct"]:
        if col in df.columns:
            df[col] = (df[col] * 100).round(2)
    return df


def generate_excel_report(result, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        # ✅ Summary
        summary_df = pd.DataFrame([result.get("summary", {})])
        summary_df = _convert_pct_columns(summary_df)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        # ✅ Store Validation
        store_df = pd.DataFrame(result.get("store_report", []))
        store_df = _convert_pct_columns(store_df)
        store_df.to_excel(writer, sheet_name="Store Validation", index=False)

        # ✅ UPC Validation
        upc_df = pd.DataFrame(result.get("upc_report", []))
        upc_df = _convert_pct_columns(upc_df)
        upc_df.to_excel(writer, sheet_name="UPC Validation", index=False)

        # ✅ Missing Stores
        missing_df = pd.DataFrame(
            result.get("missing_stores", []),
            columns=["store"]
        )
        missing_df.to_excel(writer, sheet_name="Missing Stores", index=False)

        # ✅ Extra Stores
        extra_df = pd.DataFrame(
            result.get("extra_stores", []),
            columns=["store"]
        )
        extra_df.to_excel(writer, sheet_name="Extra Stores", index=False)
