import json


def save_config(config, file_path):
    """
    Save configuration dictionary to JSON file.
    """
    with open(file_path, "w") as f:
        json.dump(config, f, indent=2)


def load_config(file_path):
    """
    Load configuration from JSON file.
    Raises FileNotFoundError if file does not exist.
    """
    with open(file_path, "r") as f:
        return json.load(f)