
import pytest

from flowpipe.transforms import (
    select_columns,
    rename_columns,
    filter_rows,
)


@pytest.fixture
def sample_rows():
    return [
        {"name": "Ali", "city": "London", "age": 25},
        {"name": "Sara", "city": "Toronto", "age": 30},
        {"name": "Reza", "city": "London", "age": 28},
    ]


def test_select_columns(sample_rows):
    result = select_columns(sample_rows, ["name", "age"])

    assert len(result) == 3
    assert result[0] == {"name": "Ali", "age": 25}


def test_select_missing_column(sample_rows):
    with pytest.raises(KeyError):
        select_columns(sample_rows, ["unknown"])


def test_select_duplicate_columns(sample_rows):
    with pytest.raises(ValueError):
        select_columns(sample_rows, ["name", "name"])


def test_rename_columns(sample_rows):
    result = rename_columns(
        sample_rows, {"name": "full_name"}
    )

    assert result[0]["full_name"] == "Ali"
    assert "name" not in result[0]


def test_rename_collision(sample_rows):
    with pytest.raises(ValueError):
        rename_columns(
            sample_rows, {"name": "city"}
        )


def test_filter_rows(sample_rows):
    result = filter_rows(
        sample_rows, "city", "London"
    )

    assert len(result) == 2
    assert result[0]["name"] == "Ali"
    assert result[1]["name"] == "Reza"


def test_filter_missing_column(sample_rows):
    with pytest.raises(KeyError):
        filter_rows(sample_rows, "country", "UK")


def test_original_data_unchanged(sample_rows):
    original = [row.copy() for row in sample_rows]

    select_columns(sample_rows, ["name"])
    rename_columns(sample_rows, {"name": "full_name"})
    filter_rows(sample_rows, "city", "London")

    assert sample_rows == original
