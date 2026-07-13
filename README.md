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

The maintenance scripts download or read source pages, convert PDF pages to plain text, extract link names and PD expressions with constrained regular expressions, discard empty artifacts, and concatenate normalized records. The committed output is data, not a runtime Python package.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

- Poppler's `pdftotext` command is required when rebuilding text from PDF files.
- Network access is required only when refreshing source pages.
- No external software is needed to consume the committed `data/pd_code_list.txt`.

## Development

Run examples and package checks before release. Python packages require Python 3.10 or newer. Build PyPI artifacts with:

```bash
poetry check
poetry build
```

## License

MIT. See `LICENSE`.
