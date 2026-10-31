
import csv
import json
from pathlib import Path


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as dictionaries."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def read_json(file_path: str | Path) -> list[dict[str, object]]:
    """Read a JSON file containing an array of objects."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("JSON input must be an array of objects.")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Every item in the JSON array must be an object.")

    return data
