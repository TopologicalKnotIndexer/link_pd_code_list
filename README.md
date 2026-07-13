# link-pd-code-list

Maintain the source material and normalized PD-code list for tabulated links.

## Installation

Clone the repository. The ready-to-use normalized file is `data/pd_code_list.txt`.

## Usage example

```python
from pathlib import Path

rows = Path("data/pd_code_list.txt").read_text(encoding="utf-8").splitlines()
name, pd_text = rows[0].split(":", 1)
print(name, pd_text.strip())
```

To rebuild extracted text:

```bash
python scripts/pdf_to_text.py
python scripts/extract_pdcode.py
```

## Algorithm

The maintenance scripts download or read source pages, convert PDF pages to plain text, extract exactly one link name/PD expression per page, discard empty artifacts, and atomically write normalized records. Any malformed or missing page stops the build instead of being silently skipped. The committed output contains 1,424 unique tabulated-link records; every name, crossing count, label range, and twice-occurrence invariant is checked by `scripts/validate_pd_code_list.py`.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

- Poppler's `pdftotext` command is required when rebuilding text from PDF files.
- Network access is required only when refreshing source pages.
- No external software is needed to consume the committed `data/pd_code_list.txt`.

## Development

Validate the committed dataset and run maintenance-script tests with Python 3.10 or newer:

```bash
python scripts/validate_pd_code_list.py
python -m unittest discover -s tests -v
```

This data repository has no PyPI publication step.

## License

MIT. See `LICENSE`.
