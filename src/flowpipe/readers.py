
import csv
import json
from pathlib import Path


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as dictionaries."""
    rows, _ = _read_csv_with_headers(file_path)
    return rows


def _read_csv_with_headers(
    file_path: str | Path,
) -> tuple[list[dict[str, str]], list[str] | None]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        return rows, reader.fieldnames


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
