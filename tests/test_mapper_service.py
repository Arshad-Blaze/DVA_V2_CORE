from services.mapper_service import map_columns


def test_basic_mapping():

    columns = [
        "STORE_NUMBER",
        "UPC_CODE",
        "ITEM_DESC",
        "UNITS_SOLD",
        "TOTAL_SALES"
    ]

    mapping = map_columns(columns)

    assert mapping["store"] == "STORE_NUMBER"
    assert mapping["upc"] == "UPC_CODE"
    assert mapping["desc"] == "ITEM_DESC"
    assert mapping["units"] == "UNITS_SOLD"
    assert mapping["dollars"] == "TOTAL_SALES"

def test_case_insensitive_mapping():

    columns = ["store", "upc", "desc", "units", "sales"]

    mapping = map_columns(columns)

    assert mapping["store"] == "store"
    assert mapping["dollars"] == "sales"

def test_alternative_names():

    columns = ["store_id", "item_code", "product_desc", "qty", "revenue"]

    mapping = map_columns(columns)

    assert mapping["store"] == "store_id"
    assert mapping["upc"] == "item_code"
    assert mapping["desc"] == "product_desc"
    assert mapping["units"] == "qty"
    assert mapping["dollars"] == "revenue"

def test_missing_fields():

    columns = ["store_id", "units"]

    mapping = map_columns(columns)

    assert mapping["store"] == "store_id"
    assert mapping["units"] == "units"

    assert mapping.get("upc") is None
    assert mapping.get("dollars") is None

