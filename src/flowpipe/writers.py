
import csv
import json
from pathlib import Path
from typing import Any


Record = dict[str, Any]


def write_csv(
    file_path: str | Path,
    rows: list[Record],
) -> None:
    """Write records into a CSV file."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8", newline="") as file:
        if not rows:
            return

        fieldnames = list(rows[0].keys())

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(
    file_path: str | Path,
    rows: list[Record],
) -> None:
    """Write records into a JSON file."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            rows,
            file,
            indent=2,
            ensure_ascii=False,
        )
