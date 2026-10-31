
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
