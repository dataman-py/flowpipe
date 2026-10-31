
"""Command-line interface for FlowPipe."""

import argparse
from pathlib import Path

from .pipeline import run_pipeline


def parse_pair(value: str) -> tuple[str, str]:
    """Parse a COLUMN=VALUE argument."""
    column, separator, item = value.partition("=")

    if not separator or not column.strip():
        raise argparse.ArgumentTypeError(
            "Expected COLUMN=VALUE."
        )

    return column.strip(), item


def parse_rename(value: str) -> tuple[str, str]:
    """Parse a SOURCE=TARGET rename argument."""
    source, target = parse_pair(value)

    if not target.strip():
        raise argparse.ArgumentTypeError(
            "Target column cannot be empty."
        )

    return source, target.strip()


def parse_columns(value: str) -> list[str]:
    """Parse comma-separated column names."""
    columns = [item.strip() for item in value.split(",")]

    if not all(columns):
        raise argparse.ArgumentTypeError(
            "Column names cannot be empty."
        )

    return columns


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="flowpipe",
        description="Transform CSV and JSON data.",
    )

    parser.add_argument(
        "--input", required=True, type=Path,
        help="Input CSV or JSON file.",
    )
    parser.add_argument(
        "--output", required=True, type=Path,
        help="Output CSV or JSON file.",
    )
    parser.add_argument(
        "--filter", type=parse_pair,
        help="Filter rows using COLUMN=VALUE.",
    )
    parser.add_argument(
        "--select", type=parse_columns,
        help="Comma-separated columns to keep.",
    )
    parser.add_argument(
        "--rename",
        type=parse_rename,
        action="append",
        default=[],
        help="Rename SOURCE=TARGET. Can be repeated.",
    )

    args = parser.parse_args(argv)

    rename_map = dict(args.rename)

    if len(rename_map) != len(args.rename):
        parser.error("Duplicate rename source columns.")

    try:
        count = run_pipeline(
            args.input,
            args.output,
            filter_by=args.filter,
            columns=args.select,
            rename_map=rename_map or None,
        )
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(
            1, f"FlowPipe error: {exc}\n"
        )

    print(
        f"Processed {count} record(s). "
        f"Output: {args.output}"
    )
    return 0
