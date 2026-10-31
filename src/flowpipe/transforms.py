
from typing import Any

Record = dict[str, Any]


def select_columns(
    rows: list[Record], columns: list[str]
) -> list[Record]:
    """Keep only the selected columns."""
    if not columns:
        raise ValueError("Column list cannot be empty.")

    if len(columns) != len(set(columns)):
        raise ValueError("Duplicate column names are not allowed.")

    result = []

    for row in rows:
        missing = [col for col in columns if col not in row]

        if missing:
            raise KeyError(f"Missing columns: {missing}")

        result.append({col: row[col] for col in columns})

    return result


def rename_columns(
    rows: list[Record], mapping: dict[str, str]
) -> list[Record]:
    """Rename columns without changing the input data."""
    result = []

    for row in rows:
        new_row = {}

        for key, value in row.items():
            new_key = mapping.get(key, key)

            if new_key in new_row:
                raise ValueError(
                    f"Column name collision: {new_key}"
                )

            new_row[new_key] = value

        result.append(new_row)

    return result


def filter_rows(
    rows: list[Record], column: str, value: Any
) -> list[Record]:
    """Keep rows where the column exactly matches a value."""
    for row in rows:
        if column not in row:
            raise KeyError(f"Column not found: {column}")

    return [
        row.copy()
        for row in rows
        if row[column] == value
    ]
