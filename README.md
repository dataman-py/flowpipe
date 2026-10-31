# FlowPipe

FlowPipe is a Python-based data transformation tool designed to simplify working with structured data.

## Overview

The project aims to provide a configurable pipeline engine for reading, transforming, validating, and exporting CSV and JSON data.

## Project Status

Early development.

## Quick Start

Requirements: Python 3.11+

Install the project:

```bash
python -m pip install -e .
```

Run a sample transformation:

```bash
flowpipe \
  --input examples/people.csv \
  --output london.json \
  --filter city=London \
  --select name,age \
  --rename name=full_name
```

Alternatively, run:

```bash
python -m flowpipe --help
```

The example filters records from London, keeps
the name and age columns, and renames name
to full_name.

## Current Capabilities

- CSV and JSON input
- Row filtering by exact equality
- Column selection and renaming
- CSV and JSON output
- Command-line interface
- Automated tests with GitHub Actions

Empty CSV results keep known column headers, including selected and renamed
columns. CSV input supplies the headers; JSON input uses the first object's
keys. If the input has no headers or objects, use `--select` to supply column
names. Without known column names, the CSV output is an empty file.

The Python function `write_csv(path, rows, fieldnames=[...])` also accepts
column names for an empty result. Duplicate column names and record keys
outside the output columns cause an error before the output file is opened.
Missing keys produce empty CSV fields.

## Known Limitations

- CSV values are treated as strings.
- Filters support exact equality only.
- Pipelines cannot yet be saved as configurations.
- Advanced validation and logging are not implemented.

## Initial Goals

- Read CSV and JSON files
- Select and rename columns
- Filter records
- Export processed data
- Provide a command-line interface
- Add automated tests

## Future Development

- Configurable multi-step pipelines
- Data validation and error reporting
- Pipeline execution history
- Scheduled processing
- Web interface
- Database connectors

## Technology

- Python
- Pytest
- YAML (planned)
- FastAPI (planned)

## Roadmap

See ROADMAP.md for upcoming development milestones.

## License

MIT License
