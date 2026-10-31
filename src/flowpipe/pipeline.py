
from pathlib import Path

from .readers import read_csv, read_json
from .transforms import (
    filter_rows,
    select_columns,
    rename_columns,
)
from .writers import write_csv, write_json


def run_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    *,
    filter_by: tuple[str, str] | None = None,
    columns: list[str] | None = None,
    rename_map: dict[str, str] | None = None,
) -> int:
    """Run a data transformation pipeline."""

    input_path = Path(input_path)
    output_path = Path(output_path)

    # Load input data
    input_format = input_path.suffix.lower()

    if input_format == ".csv":
        rows = read_csv(input_path)
    elif input_format == ".json":
        rows = read_json(input_path)
    else:
        raise ValueError(
            f"Unsupported input format: {input_format}"
        )

    # Apply transformations in order
    if filter_by is not None:
        column, value = filter_by
        rows = filter_rows(rows, column, value)

    if columns is not None:
        rows = select_columns(rows, columns)

    if rename_map is not None:
        rows = rename_columns(rows, rename_map)

    # Save the result
    output_format = output_path.suffix.lower()

    if output_format == ".csv":
        write_csv(output_path, rows)
    elif output_format == ".json":
        write_json(output_path, rows)
    else:
        raise ValueError(
            f"Unsupported output format: {output_format}"
        )

    return len(rows)
