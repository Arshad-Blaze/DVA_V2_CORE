from services.config_service import save_config, load_config

def test_save_config(tmp_path):
    import json

    config = {
        "mapping": {"store": "store_id"},
        "units_implied": True
    }

    file_path = tmp_path / "config.json"

    save_config(config, file_path)

    assert file_path.exists()

    with open(file_path) as f:
        data = json.load(f)

    assert data["mapping"]["store"] == "store_id"

def test_load_config(tmp_path):
    
    import json

    file_path = tmp_path / "config.json"

    config = {"units_implied": True}

    with open(file_path, "w") as f:
        json.dump(config, f)

    loaded = load_config(file_path)

    assert loaded["units_implied"] is True

def test_config_round_trip(tmp_path):

    config = {
        "mapping": {
            "store": "store_id",
            "units": "qty"
        },
        "dollars_implied": True
    }

    file_path = tmp_path / "config.json"

    save_config(config, file_path)
    loaded = load_config(file_path)

    assert loaded == config

def test_load_config_missing_file(tmp_path):
    
    import pytest

    file_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_config(file_path)

