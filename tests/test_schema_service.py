import pandas as pd
import os
from services.schema_service import get_schema
import pyarrow.parquet as pq

def test_schema_basic(tmp_path):
    file_path = tmp_path / "test.parquet"

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", None],
        "amount": [10.5, None, 30.0]
    })

    df.to_parquet(file_path, index=False)

    schema = get_schema(file_path)

    assert isinstance(schema, list)
    assert len(schema) == 3

    cols = {col["column"]: col for col in schema}

    assert "id" in cols
    assert cols["id"]["dtype"] in ["int64", "int32"]
    assert cols["id"]["null_count"] == 0
    assert cols["id"]["sample_value"] == 1

    assert "name" in cols
    assert cols["name"]["null_count"] == 1

    assert "amount" in cols
    assert cols["amount"]["null_count"] == 1


def test_schema_empty_file(tmp_path):
    file_path = tmp_path / "empty.parquet"

    df = pd.DataFrame(columns=["a", "b"])
    df.to_parquet(file_path, index=False)

    schema = get_schema(file_path)

    assert len(schema) == 2

    for col in schema:
        assert col["null_count"] == 0
        assert col["sample_value"] is None


def test_schema_large_file_sampling(tmp_path):
    file_path = tmp_path / "large.parquet"

    df = pd.DataFrame({
        "col": list(range(1000))
    })

    df.to_parquet(file_path, index=False)

    schema = get_schema(file_path)

    assert len(schema) == 1
    assert schema[0]["sample_value"] == 0


def test_schema_uses_metadata_not_full_read(tmp_path, monkeypatch):
    file_path = tmp_path / "test.parquet"

    import pandas as pd
    df = pd.DataFrame({
        "a": list(range(1000)),
        "b": ["x"] * 1000
    })
    df.to_parquet(file_path, index=False)

    # 🔴 Force pandas.read_parquet to fail if called fully
    def fail_read(*args, **kwargs):
        raise RuntimeError("Full read should not be used")

    monkeypatch.setattr(pd, "read_parquet", fail_read)

    from services.schema_service import get_schema

    schema = get_schema(file_path)

    assert len(schema) == 2
    cols = {c["column"]: c for c in schema}

    assert "a" in cols
    assert "b" in cols


def test_schema_sample_from_small_read(tmp_path):
    file_path = tmp_path / "sample.parquet"

    import pandas as pd
    df = pd.DataFrame({
        "col": [None, None, 5, 6]
    })
    df.to_parquet(file_path, index=False)

    from services.schema_service import get_schema

    schema = get_schema(file_path)

    assert schema[0]["sample_value"] == 5