import csv

import pytest

from flowpipe.writers import write_csv


@pytest.mark.parametrize("fieldnames, expected", [
    (None, ""),
    (["name", "city"], "name,city\n"),
])
def test_write_empty_csv(tmp_path, fieldnames, expected):
    target = tmp_path / "output.csv"

    write_csv(target, [], fieldnames=fieldnames)

    assert target.read_text(encoding="utf-8") == expected


@pytest.mark.parametrize("rows, fieldnames", [
    ([{"name": "Ali"}, {"name": "Sara", "city": "Toronto"}], None),
    ([{"name": "Ali", "city": "London"}], ["name"]),
    ([], ["name", "name"]),
])
def test_invalid_columns_preserve_output(tmp_path, rows, fieldnames):
    target = tmp_path / "output.csv"
    target.write_text("keep this file\n", encoding="utf-8")

    with pytest.raises(ValueError):
        write_csv(target, rows, fieldnames=fieldnames)

    assert target.read_text(encoding="utf-8") == "keep this file\n"


def test_write_csv_column_order_and_missing_keys(tmp_path):
    target = tmp_path / "output.csv"

    write_csv(target, [{"name": "Ali", "city": "London"}, {"name": "Sara"}],
              fieldnames=["city", "name"])

    with target.open(newline="", encoding="utf-8") as file:
        assert list(csv.reader(file)) == [["city", "name"], ["London", "Ali"], ["", "Sara"]]


def test_write_csv_empty_records(tmp_path):
    target = tmp_path / "output.csv"

    write_csv(target, [{}])

    assert target.read_text(encoding="utf-8") == "\n\n"
