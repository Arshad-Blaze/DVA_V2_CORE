import pandas as pd
from services.validation_service import validate_stores

def test_store_validation_aggregation_basic(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1, 1, 2],
        "units": [10, 20, 30],
        "dollars": [100, 200, 300]
    })

    df_test = pd.DataFrame({
        "store_id": [1, 2, 2],
        "units": [15, 25, 5],
        "dollars": [150, 250, 50]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        store_column="store_id",
        units_column="units",
        dollars_column="dollars"
    )

    # ✅ Summary
    assert result["summary"]["bau_units"] == 60
    assert result["summary"]["test_units"] == 45

    # ✅ Store-level
    store_data = {r["store"]: r for r in result["store_report"]}

    # Store 1
    assert store_data[1]["units_diff"] == (30 - 15)

    # Store 2
    assert store_data[2]["units_diff"] == (30 - 30)

    # ✅ Missing / extra stores
    assert result["missing_stores"] == []
    assert result["extra_stores"] == []

def test_store_validation_missing_extra(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1, 2],
        "units": [10, 20],
        "dollars": [100, 200]
    })

    df_test = pd.DataFrame({
        "store_id": [2, 3],
        "units": [20, 30],
        "dollars": [200, 300]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        "store_id",
        "units",
        "dollars"
    )

    assert result["missing_stores"] == [1]
    assert result["extra_stores"] == [3]

def test_upc_validation_basic(tmp_path):
    import pandas as pd
    from services.validation_service import validate_upc

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "upc": ["A", "A", "B"],
        "units": [10, 20, 30],
        "dollars": [100, 200, 300]
    })

    df_test = pd.DataFrame({
        "upc": ["A", "B", "B"],
        "units": [15, 25, 5],
        "dollars": [150, 250, 50]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_upc(
        bau_path,
        test_path,
        upc_column="upc",
        units_column="units",
        dollars_column="dollars"
    )

    # ✅ Summary
    assert result["summary"]["bau_units"] == 60
    assert result["summary"]["test_units"] == 45

    report = {r["upc"]: r for r in result["upc_report"]}

    # UPC A: BAU = 30, TEST = 15
    assert report["A"]["units_diff"] == 15

    # UPC B: BAU = 30, TEST = 30
    assert report["B"]["units_diff"] == 0

def test_upc_validation_with_store_desc(tmp_path):
    import pandas as pd
    from services.validation_service import validate_upc

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store": [1, 1, 2],
        "upc": ["A", "B", "A"],
        "desc": ["item", "item", "item"],
        "units": [10, 20, 30],
        "dollars": [100, 200, 300]
    })

    df_test = pd.DataFrame({
        "store": [1, 2],
        "upc": ["A", "A"],
        "desc": ["item", "item"],
        "units": [15, 25],
        "dollars": [150, 250]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_upc(
        bau_path,
        test_path,
        upc_column="upc",
        units_column="units",
        dollars_column="dollars",
        store_column="store",
        desc_column="desc"
    )

    assert len(result["upc_report"]) > 0

def test_units_pct_zero_division(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1],
        "units": [0],
        "dollars": [0]
    })

    df_test = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "dollars": [100]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        "store_id",
        "units",
        "dollars"
    )

    # ✅ Should NOT crash and pct should be 0
    assert result["summary"]["units_pct"] == 0

def test_store_only_in_test(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "dollars": [100]
    })

    df_test = pd.DataFrame({
        "store_id": [1, 2],
        "units": [10, 20],
        "dollars": [100, 200]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        "store_id",
        "units",
        "dollars"
    )

    # ✅ Store 2 should appear as extra
    assert result["extra_stores"] == [2]

def test_upc_only_in_test(tmp_path):
    import pandas as pd
    from services.validation_service import validate_upc

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "upc": ["A"],
        "units": [10],
        "dollars": [100]
    })

    df_test = pd.DataFrame({
        "upc": ["A", "B"],
        "units": [10, 20],
        "dollars": [100, 200]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_upc(
        bau_path,
        test_path,
        "upc",
        "units",
        "dollars"
    )

    upcs = [r["upc"] for r in result["upc_report"]]

    assert "B" in upcs

def test_large_values_precision(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1],
        "units": [1_000_000_000],
        "dollars": [5_000_000_000]
    })

    df_test = pd.DataFrame({
        "store_id": [1],
        "units": [999_000_000],
        "dollars": [4_990_000_000]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        "store_id",
        "units",
        "dollars"
    )

    assert result["summary"]["units_diff"] == 1_000_000

def test_all_zero_values(tmp_path):
    import pandas as pd
    from services.validation_service import validate_upc

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "upc": ["A"],
        "units": [0],
        "dollars": [0]
    })

    df_test = pd.DataFrame({
        "upc": ["A"],
        "units": [0],
        "dollars": [0]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_upc(
        bau_path,
        test_path,
        "upc",
        "units",
        "dollars"
    )

    assert result["summary"]["units_pct"] == 0

def test_store_report_structure(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "dollars": [100]
    })

    df.to_parquet(bau_path, index=False)
    df.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path, test_path,
        "store_id", "units", "dollars"
    )

    row = result["store_report"][0]

    expected_keys = {
        "store",
        "bau_units",
        "test_units",
        "units_diff",
        "units_pct",
        "bau_dollars",
        "test_dollars",
        "dollars_diff",
        "dollars_pct"
    }

    assert expected_keys.issubset(set(row.keys()))

def test_summary_structure(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    path = tmp_path / "file.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "dollars": [100]
    })

    df.to_parquet(path, index=False)

    result = validate_stores(
        path, path,
        "store_id", "units", "dollars"
    )

    summary = result["summary"]

    expected_keys = {
        "bau_units",
        "test_units",
        "units_diff",
        "units_pct",
        "bau_dollars",
        "test_dollars",
        "dollars_diff",
        "dollars_pct"
    }

    assert expected_keys.issubset(set(summary.keys()))

def test_upc_report_structure(tmp_path):
    import pandas as pd
    from services.validation_service import validate_upc

    path = tmp_path / "file.parquet"

    df = pd.DataFrame({
        "upc": ["A"],
        "units": [10],
        "dollars": [100]
    })

    df.to_parquet(path, index=False)

    result = validate_upc(
        path, path,
        "upc", "units", "dollars"
    )

    row = result["upc_report"][0]

    expected_keys = {
        "upc",
        "bau_units",
        "test_units",
        "units_diff",
        "units_pct",
        "bau_dollars",
        "test_dollars",
        "dollars_diff",
        "dollars_pct"
    }

    assert expected_keys.issubset(set(row.keys()))

def test_store_report_sorted(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [3, 1, 2],
        "units": [10, 20, 30],
        "dollars": [100, 200, 300]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_bau.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path, test_path,
        "store_id", "units", "dollars"
    )

    stores = [r["store"] for r in result["store_report"]]

    assert stores == sorted(stores)

def test_no_nulls_in_report(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "dollars": [100]
    })

    df_test = pd.DataFrame({
        "store_id": [2],
        "units": [20],
        "dollars": [200]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path, test_path,
        "store_id", "units", "dollars"
    )

    for row in result["store_report"]:
        for value in row.values():
            assert value is not None

def test_unit_price_derivation(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "unit_price": [5]
    })

    df_test = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "unit_price": [4]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores(
        bau_path,
        test_path,
        store_column="store_id",
        units_column="units",
        dollars_column=None,              # ✅ missing
        unit_price_column="unit_price"    # ✅ new
    )

    # BAU dollars = 10 * 5 = 50
    # TEST dollars = 10 * 4 = 40
    assert result["summary"]["bau_dollars"] == 50
    assert result["summary"]["test_dollars"] == 40

def test_units_implied_scaling(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    path = tmp_path / "file.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [1000],   # actually 10.00
        "dollars": [2000]  # actually 20.00
    })

    df.to_parquet(path, index=False)

    result = validate_stores(
        path,
        path,
        store_column="store_id",
        units_column="units",
        dollars_column="dollars",
        units_implied=True,
        dollars_implied=True
    )

    assert result["summary"]["bau_units"] == 10
    assert result["summary"]["bau_dollars"] == 20

def test_unit_price_with_implied(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores

    path = tmp_path / "file.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [1000],        # → 10
        "unit_price": [500]     # → 5
    })

    df.to_parquet(path, index=False)

    result = validate_stores(
        path,
        path,
        store_column="store_id",
        units_column="units",
        dollars_column=None,
        unit_price_column="unit_price",
        units_implied=True,
        unit_price_implied=True
    )

    # 10 * 5 = 50
    assert result["summary"]["bau_dollars"] == 50

def test_missing_price_fields(tmp_path):
    import pandas as pd
    import pytest
    from services.validation_service import validate_stores

    path = tmp_path / "file.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [10]
    })

    df.to_parquet(path, index=False)

    with pytest.raises(ValueError):
        validate_stores(
            path,
            path,
            "store_id",
            "units",
            dollars_column=None
        )

def test_validate_stores_auto_basic(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    bau_path = tmp_path / "bau.parquet"
    test_path = tmp_path / "test.parquet"

    df_bau = pd.DataFrame({
        "STORE_NUMBER": [1],
        "UNITS_SOLD": [10],
        "TOTAL_SALES": [100]
    })

    df_test = pd.DataFrame({
        "STORE_NUMBER": [1],
        "UNITS_SOLD": [8],
        "TOTAL_SALES": [80]
    })

    df_bau.to_parquet(bau_path, index=False)
    df_test.to_parquet(test_path, index=False)

    result = validate_stores_auto(bau_path, test_path)

    assert result["summary"]["bau_units"] == 10
    assert result["summary"]["test_units"] == 8

def test_validate_stores_auto_unit_price(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "unit_price": [5]
    })

    df.to_parquet(path, index=False)

    result = validate_stores_auto(path, path)

    assert result["summary"]["bau_dollars"] == 50

def test_validate_stores_auto_with_implied(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store": [1],
        "units": [1000],     # → 10
        "sales": [2000]      # → 20
    })

    df.to_parquet(path, index=False)

    result = validate_stores_auto(
        path,
        path,
        config={
            "units_implied": True,
            "dollars_implied": True
        }
    )

    assert result["summary"]["bau_units"] == 10
    assert result["summary"]["bau_dollars"] == 20

def test_validate_stores_auto_missing_fields(tmp_path):
    import pandas as pd
    import pytest
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store_id": [1]
    })

    df.to_parquet(path, index=False)

    with pytest.raises(ValueError):
        validate_stores_auto(path, path)

def test_validate_stores_auto_with_mapping_config(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "CUSTOM_STORE": [1],
        "CUSTOM_UNITS": [10],
        "CUSTOM_SALES": [100]
    })

    df.to_parquet(path, index=False)

    config = {
        "mapping": {
            "store": "CUSTOM_STORE",
            "units": "CUSTOM_UNITS",
            "dollars": "CUSTOM_SALES"
        }
    }

    result = validate_stores_auto(path, path, config=config)

    assert result["summary"]["bau_units"] == 10
    assert result["summary"]["bau_dollars"] == 100

def test_config_overrides_mapper(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store_id": [1],
        "units": [10],
        "sales": [100]
    })

    df.to_parquet(path, index=False)

    # Intentionally override mapping
    config = {
        "mapping": {
            "store": "store_id",
            "units": "units",
            "dollars": "sales"
        }
    }

    result = validate_stores_auto(path, path, config=config)

    assert result["summary"]["bau_dollars"] == 100

def test_validate_stores_auto_config_unit_price(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store": [1],
        "qty": [10],
        "price": [5]
    })

    df.to_parquet(path, index=False)

    config = {
        "mapping": {
            "store": "store",
            "units": "qty",
            "unit_price": "price"
        }
    }

    result = validate_stores_auto(path, path, config=config)

    assert result["summary"]["bau_dollars"] == 50

def test_validate_stores_auto_config_with_implied(tmp_path):
    import pandas as pd
    from services.validation_service import validate_stores_auto

    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store": [1],
        "qty": [1000],       # → 10
        "sales": [2000]      # → 20
    })

    df.to_parquet(path, index=False)

    config = {
        "mapping": {
            "store": "store",
            "units": "qty",
            "dollars": "sales"
        },
        "units_implied": True,
        "dollars_implied": True
    }

    result = validate_stores_auto(path, path, config=config)

    assert result["summary"]["bau_units"] == 10
    assert result["summary"]["bau_dollars"] == 20

import pandas as pd
from services.validation_service import validate_stores


def test_validation_large_dataset(tmp_path):
    path = tmp_path / "data.parquet"

    df = pd.DataFrame({
        "store_id": [1] * 1000,
        "units": [1] * 1000,
        "dollars": [2] * 1000
    })

    df.to_parquet(path)

    result = validate_stores(
        path,
        path,
        store_column="store_id",
        units_column="units",
        dollars_column="dollars"
    )

    assert result["summary"]["bau_units"] == 1000
    assert result["summary"]["bau_dollars"] == 2000