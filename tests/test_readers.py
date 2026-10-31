
import json

import pytest

from flowpipe.readers import read_csv, read_json


def test_read_csv(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text(
        "name,city\nAli,London\nSara,Toronto\n",
        encoding="utf-8",
    )

    result = read_csv(file_path)

    assert len(result) == 2
    assert result[0]["name"] == "Ali"
    assert result[1]["city"] == "Toronto"


def test_read_json(tmp_path):
    file_path = tmp_path / "sample.json"
    data = [{"name": "Ali", "city": "London"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_json(file_path)

    assert result == data


def test_invalid_json_structure(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"name": "Ali"}', encoding="utf-8")

    with pytest.raises(ValueError):
        read_json(file_path)


def test_missing_csv_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_csv(tmp_path / "missing.csv")


@pytest.mark.parametrize("content", ["", "name,city\n"])
def test_empty_csv_returns_plain_list(tmp_path, content):
    file_path = tmp_path / "empty.csv"
    file_path.write_text(content, encoding="utf-8")

    result = read_csv(file_path)

    assert type(result) is list
    assert result == []
