def map_columns(columns):
    mapping = {
        "store": None,
        "upc": None,
        "desc": None,
        "units": None,
        "dollars": None,
        "unit_price": None   # ✅ NEW
    }

    col_map = {col: col.lower() for col in columns}

    for original, col in col_map.items():

        # ✅ STORE
        if mapping["store"] is None and "store" in col:
            mapping["store"] = original

        # ✅ UPC
        elif mapping["upc"] is None and any(k in col for k in ["upc", "item", "sku", "code"]):
            mapping["upc"] = original

        # ✅ DESCRIPTION
        elif mapping["desc"] is None and any(k in col for k in ["desc", "description"]):
            mapping["desc"] = original

        # ✅ UNITS
        elif mapping["units"] is None and any(k in col for k in ["unit", "qty", "quantity"]):
            mapping["units"] = original

        # ✅ UNIT PRICE (✅ NEW)
        elif mapping["unit_price"] is None and "price" in col:
            mapping["unit_price"] = original

        # ✅ DOLLARS
        elif mapping["dollars"] is None and any(k in col for k in ["sale", "amount", "dollar", "revenue"]):
            mapping["dollars"] = original

    return mapping