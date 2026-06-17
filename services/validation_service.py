from services.load_dataframe_service import load_dataframe


def validate_stores(
    bau_path,
    test_path,
    store_column,
    units_column,
    dollars_column=None,
    unit_price_column=None,
    units_implied=False,
    dollars_implied=False,
    unit_price_implied=False
):
    df_bau = load_dataframe(bau_path)
    df_test = load_dataframe(test_path)

    # ✅ Rename base columns
    rename_map = {
        store_column: "store",
        units_column: "units"
    }

    if dollars_column:
        rename_map[dollars_column] = "dollars"

    if unit_price_column:
        rename_map[unit_price_column] = "unit_price"

    df_bau = df_bau.rename(columns=rename_map)
    df_test = df_test.rename(columns=rename_map)

    # ✅ Apply implied scaling
    if units_implied:
        df_bau["units"] /= 100
        df_test["units"] /= 100

    if dollars_implied and "dollars" in df_bau.columns:
        df_bau["dollars"] /= 100
        df_test["dollars"] /= 100

    if unit_price_implied and "unit_price" in df_bau.columns:
        df_bau["unit_price"] /= 100
        df_test["unit_price"] /= 100

    # ✅ Derive dollars if missing
    if "dollars" not in df_bau.columns:
        if "unit_price" in df_bau.columns:
            df_bau["dollars"] = df_bau["units"] * df_bau["unit_price"]
            df_test["dollars"] = df_test["units"] * df_test["unit_price"]
        else:
            raise ValueError("No dollars or unit_price column provided")

    # ✅ Continue EXISTING logic unchanged
    bau_agg = (
        df_bau
        .groupby("store", as_index=False)
        .agg({"units": "sum", "dollars": "sum"})
        .rename(columns={
            "units": "bau_units",
            "dollars": "bau_dollars"
        })
    )

    test_agg = (
        df_test
        .groupby("store", as_index=False)
        .agg({"units": "sum", "dollars": "sum"})
        .rename(columns={
            "units": "test_units",
            "dollars": "test_dollars"
        })
    )

    merged = bau_agg.merge(test_agg, on="store", how="outer").fillna(0)

    merged["units_diff"] = merged["bau_units"] - merged["test_units"]
    merged["dollars_diff"] = merged["bau_dollars"] - merged["test_dollars"]

    merged["units_pct"] = merged.apply(
        lambda x: x["units_diff"] / x["bau_units"]
        if x["bau_units"] != 0 else 0,
        axis=1
    )

    merged["dollars_pct"] = merged.apply(
        lambda x: x["dollars_diff"] / x["bau_dollars"]
        if x["bau_dollars"] != 0 else 0,
        axis=1
    )

    # ✅ Store lists
    bau_stores = set(bau_agg["store"])
    test_stores = set(test_agg["store"])

    missing_stores = sorted(list(bau_stores - test_stores))
    extra_stores = sorted(list(test_stores - bau_stores))

    # ✅ Summary
    summary = {
        "bau_units": bau_agg["bau_units"].sum(),
        "test_units": test_agg["test_units"].sum(),
        "bau_dollars": bau_agg["bau_dollars"].sum(),
        "test_dollars": test_agg["test_dollars"].sum()
    }

    summary["units_diff"] = summary["bau_units"] - summary["test_units"]
    summary["dollars_diff"] = summary["bau_dollars"] - summary["test_dollars"]

    summary["units_pct"] = (
        summary["units_diff"] / summary["bau_units"]
        if summary["bau_units"] != 0 else 0
    )

    summary["dollars_pct"] = (
        summary["dollars_diff"] / summary["bau_dollars"]
        if summary["bau_dollars"] != 0 else 0
    )

    store_report = merged.sort_values("store").to_dict(orient="records")

    return {
        "summary": summary,
        "missing_stores": missing_stores,
        "extra_stores": extra_stores,
        "store_report": store_report
    }

def validate_upc(
    bau_path,
    test_path,
    upc_column,
    units_column,
    dollars_column,
    store_column=None,
    desc_column=None
):
    df_bau = load_dataframe(bau_path)
    df_test = load_dataframe(test_path)

    # ✅ Normalize base columns
    rename_map = {
        upc_column: "upc",
        units_column: "units",
        dollars_column: "dollars"
    }

    if store_column:
        rename_map[store_column] = "store"

    if desc_column:
        rename_map[desc_column] = "desc"

    df_bau = df_bau.rename(columns=rename_map)
    df_test = df_test.rename(columns=rename_map)

    # ✅ Decide grouping
    group_cols = ["upc"]

    if store_column:
        group_cols.insert(0, "store")

    if desc_column:
        group_cols.append("desc")

    # ✅ Aggregate
    bau_agg = (
        df_bau
        .groupby(group_cols, as_index=False)
        .agg({"units": "sum", "dollars": "sum"})
        .rename(columns={
            "units": "bau_units",
            "dollars": "bau_dollars"
        })
    )

    test_agg = (
        df_test
        .groupby(group_cols, as_index=False)
        .agg({"units": "sum", "dollars": "sum"})
        .rename(columns={
            "units": "test_units",
            "dollars": "test_dollars"
        })
    )

    # ✅ Merge
    merged = bau_agg.merge(test_agg, on=group_cols, how="outer").fillna(0)

    # ✅ Metrics
    merged["units_diff"] = merged["bau_units"] - merged["test_units"]
    merged["dollars_diff"] = merged["bau_dollars"] - merged["test_dollars"]

    # ✅ % calculations
    merged["units_pct"] = merged.apply(
        lambda x: x["units_diff"] / x["bau_units"]
        if x["bau_units"] != 0 else 0,
        axis=1
    )

    merged["dollars_pct"] = merged.apply(
        lambda x: x["dollars_diff"] / x["bau_dollars"]
        if x["bau_dollars"] != 0 else 0,
        axis=1
    )

    # ✅ Summary
    summary = {
        "bau_units": bau_agg["bau_units"].sum(),
        "test_units": test_agg["test_units"].sum(),
        "bau_dollars": bau_agg["bau_dollars"].sum(),
        "test_dollars": test_agg["test_dollars"].sum()
    }

    summary["units_diff"] = summary["bau_units"] - summary["test_units"]
    summary["dollars_diff"] = summary["bau_dollars"] - summary["test_dollars"]

    summary["units_pct"] = (
        summary["units_diff"] / summary["bau_units"]
        if summary["bau_units"] != 0 else 0
    )

    summary["dollars_pct"] = (
        summary["dollars_diff"] / summary["bau_dollars"]
        if summary["bau_dollars"] != 0 else 0
    )

    return {
        "summary": summary,
        "upc_report": merged.to_dict(orient="records")
    }

from services.mapper_service import map_columns


def validate_stores_auto(bau_path, test_path, config=None):
    config = config or {}

    # ✅ Load data
    df_sample = load_dataframe(bau_path)

    # ✅ Map columns
    mapping = map_columns(df_sample.columns)

    store_column = mapping.get("store")
    units_column = mapping.get("units")
    dollars_column = mapping.get("dollars")
    unit_price_column = mapping.get("unit_price")  # may be None

    # ✅ Validation of required fields
    if store_column is None or units_column is None:
        raise ValueError("Missing required store or units column")

    if dollars_column is None and unit_price_column is None:
        raise ValueError("Missing both dollars and unit_price columns")

    # ✅ Extract config flags
    units_implied = config.get("units_implied", False)
    dollars_implied = config.get("dollars_implied", False)
    unit_price_implied = config.get("unit_price_implied", False)

    # ✅ Call existing validated logic
    return validate_stores(
        bau_path,
        test_path,
        store_column=store_column,
        units_column=units_column,
        dollars_column=dollars_column,
        unit_price_column=unit_price_column,
        units_implied=units_implied,
        dollars_implied=dollars_implied,
        unit_price_implied=unit_price_implied
    )

