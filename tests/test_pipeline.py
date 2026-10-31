
import csv
import json

import pytest

from flowpipe.pipeline import run_pipeline


def test_csv_to_json_pipeline(tmp_path):
    input_file = tmp_path / "people.csv"
    output_file = tmp_path / "result.json"

    input_file.write_text(
        "name,city,age\n"
        "Ali,London,25\n"
        "Sara,Toronto,30\n"
        "Reza,London,28\n",
        encoding="utf-8",
    )

    count = run_pipeline(
        input_file,
        output_file,
        filter_by=("city", "London"),
        columns=["name", "age"],
        rename_map={"name": "full_name"},
    )

    result = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert count == 2
    assert result == [
        {"full_name": "Ali", "age": "25"},
        {"full_name": "Reza", "age": "28"},
    ]


def test_json_to_csv_pipeline(tmp_path):
    input_file = tmp_path / "people.json"
    output_file = tmp_path / "result.csv"

    data = [
        {"name": "Ali", "score": 90},
        {"name": "Sara", "score": 85},
    ]

    input_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    count = run_pipeline(input_file, output_file)

    with output_file.open(
        "r", encoding="utf-8", newline=""
    ) as file:
        result = list(csv.DictReader(file))

    assert count == 2
    assert result == [
        {"name": "Ali", "score": "90"},
        {"name": "Sara", "score": "85"},
    ]


def test_unsupported_input_format(tmp_path):
    input_file = tmp_path / "data.txt"
    output_file = tmp_path / "result.csv"

    with pytest.raises(ValueError):
        run_pipeline(input_file, output_file)


def test_unsupported_output_format(tmp_path):
    input_file = tmp_path / "data.json"
    output_file = tmp_path / "result.txt"

    input_file.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        run_pipeline(input_file, output_file)


def test_empty_filtered_result(tmp_path):
    input_file = tmp_path / "people.json"
    output_file = tmp_path / "result.json"

    input_file.write_text(
        '[{"name": "Ali", "city": "London"}]',
        encoding="utf-8",
    )

    count = run_pipeline(
        input_file,
        output_file,
        filter_by=("city", "Paris"),
    )

    assert count == 0
    assert json.loads(output_file.read_text()) == []


@pytest.mark.parametrize("content", [
    "name,city\nAli,London\n",
    "name,city\n",
])
@pytest.mark.parametrize("options, expected", [
    ({}, ["name", "city"]),
    ({"columns": ["city", "name"], "rename_map": {"name": "person"}},
     ["city", "person"]),
])
def test_empty_csv_headers(tmp_path, content, options, expected):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"
    source.write_text(content, encoding="utf-8")

    count = run_pipeline(source, target, filter_by=("city", "Paris"), **options)

    assert count == 0
    with target.open(newline="", encoding="utf-8") as file:
        assert list(csv.reader(file)) == [expected]


@pytest.mark.parametrize("suffix, content, options, expected", [
    (".json", '[{"name": "Ali", "city": "London"}]',
     {"filter_by": ("city", "Paris")}, "name,city\n"),
    (".json", "[]", {"columns": ["name"], "rename_map": {"name": "person"}},
     "person\n"),
    (".csv", "", {"columns": ["name"]}, "name\n"),
    (".json", "[]", {}, ""),
    (".csv", "", {}, ""),
])
def test_empty_csv_column_sources(tmp_path, suffix, content, options, expected):
    source = tmp_path / ("input" + suffix)
    target = tmp_path / "output.csv"
    source.write_text(content, encoding="utf-8")

    assert run_pipeline(source, target, **options) == 0
    assert target.read_text(encoding="utf-8") == expected


@pytest.mark.parametrize("content, options, error", [
    ("name,city\n", {"columns": ["missing"]}, KeyError),
    ("name,city\n", {"rename_map": {"name": "city"}}, ValueError),
    ("name,name\n", {"rename_map": {"name": "person"}}, ValueError),
])
def test_empty_csv_invalid_columns_preserve_output(tmp_path, content, options, error):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"
    source.write_text(content, encoding="utf-8")
    target.write_text("keep this file\n", encoding="utf-8")

    with pytest.raises(error):
        run_pipeline(source, target, **options)

    assert target.read_text(encoding="utf-8") == "keep this file\n"


def test_json_filter_uses_remaining_columns(tmp_path):
    source = tmp_path / "input.json"
    target = tmp_path / "output.csv"
    source.write_text(
        '[{"name": "Ali"}, {"name": "Sara", "city": "Toronto"}]',
        encoding="utf-8",
    )

    assert run_pipeline(source, target, filter_by=("name", "Sara")) == 1
    with target.open(newline="", encoding="utf-8") as file:
        assert list(csv.DictReader(file)) == [{"name": "Sara", "city": "Toronto"}]
