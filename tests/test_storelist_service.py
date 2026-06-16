import pandas as pd

from services.storelist_service import (
    compare_storelist
)


def test_storelist_compare():

    retailer = pd.DataFrame({
        "Store": [
            "1001",
            "1002",
            "1003"
        ]
    })

    storelist = pd.DataFrame({
        "Store": [
            "1001",
            "1002",
            "1004"
        ]
    })

    result = compare_storelist(
        retailer_df=retailer,
        storelist_df=storelist,
        retailer_store_column="Store",
        storelist_column="Store"
    )

    assert result["matched"] == 2

    assert result["missing_in_storelist"] == [
        "1003"
    ]

    assert result["missing_in_retailer"] == [
        "1004"
    ]
def test_storelist_trim_spaces():

    retailer = pd.DataFrame({
        "Store": [
            "1001 ",
            " 1002"
        ]
    })

    storelist = pd.DataFrame({
        "Store": [
            "1001",
            "1002"
        ]
    })

    result = compare_storelist(
        retailer,
        storelist,
        "Store",
        "Store"
    )

    assert result["matched"] == 2
