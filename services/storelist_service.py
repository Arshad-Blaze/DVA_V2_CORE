def compare_storelist(
    retailer_df,
    storelist_df,
    retailer_store_column,
    storelist_column
):

    retailer_stores = (
        retailer_df[retailer_store_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    storelist_stores = (
        storelist_df[storelist_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    retailer_set = set(retailer_stores)
    storelist_set = set(storelist_stores)

    matched = retailer_set & storelist_set

    missing_in_storelist = retailer_set - storelist_set

    missing_in_retailer = storelist_set - retailer_set

    return {
        "matched": len(matched),
        "missing_in_storelist": sorted(
            list(missing_in_storelist)
        ),
        "missing_in_retailer": sorted(
            list(missing_in_retailer)
        )
    }
