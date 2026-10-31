
import csv
import json
from pathlib import Path
from typing import Any


Record = dict[str, Any]


def write_csv(
    file_path: str | Path,
    rows: list[Record],
    *,
    fieldnames: list[str] | None = None,
) -> None:
    """Write records with optional column names for an empty result."""
    path = Path(file_path)

    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []

    if len(fieldnames) != len(set(fieldnames)):
        raise ValueError("Duplicate column names are not allowed.")

    fields = set(fieldnames)
    for row in rows:
        extra = row.keys() - fields
        if extra:
            raise ValueError(f"Fields not in CSV header: {extra}")

    with path.open("w", encoding="utf-8", newline="") as file:
        if not fieldnames and not rows:
            return

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
