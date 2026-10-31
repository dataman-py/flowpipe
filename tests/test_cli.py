
import json

import pytest

from flowpipe.cli import main


def test_cli_processes_csv(tmp_path, capsys):
    source = tmp_path / "people.csv"
    target = tmp_path / "output.json"

    source.write_text(
        "name,city,age\n"
        "Ali,London,25\n"
        "Sara,Toronto,30\n"
        "Reza,London,28\n",
        encoding="utf-8",
    )

    code = main([
        "--input", str(source),
        "--output", str(target),
        "--filter", "city=London",
        "--select", "name,age",
        "--rename", "name=full_name",
    ])

    result = json.loads(target.read_text(encoding="utf-8"))

    assert code == 0
    assert result == [
        {"full_name": "Ali", "age": "25"},
        {"full_name": "Reza", "age": "28"},
    ]
    assert "Processed 2 record(s)" in capsys.readouterr().out


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])

    assert exc.value.code == 0
    assert "usage:" in capsys.readouterr().out


def test_cli_invalid_filter():
    with pytest.raises(SystemExit) as exc:
        main([
            "--input", "input.csv",
            "--output", "output.json",
            "--filter", "invalid",
        ])

    assert exc.value.code == 2


def test_cli_missing_file(tmp_path):
    with pytest.raises(SystemExit) as exc:
        main([
            "--input", str(tmp_path / "missing.csv"),
            "--output", str(tmp_path / "output.json"),
        ])

    assert exc.value.code == 1


def test_cli_invalid_rename():
    with pytest.raises(SystemExit) as exc:
        main([
            "--input", "input.csv",
            "--output", "output.json",
            "--rename", "name=",
        ])

    assert exc.value.code == 2


def test_cli_empty_csv_headers(tmp_path, capsys):
    source = tmp_path / "people.csv"
    target = tmp_path / "output.csv"
    source.write_text("name,city\nAli,London\n", encoding="utf-8")

    code = main([
        "--input", str(source), "--output", str(target),
        "--filter", "city=Paris", "--select", "name", "--rename", "name=person",
    ])

    assert code == 0
    assert target.read_text(encoding="utf-8") == "person\n"
    assert "Processed 0 record(s)" in capsys.readouterr().out
