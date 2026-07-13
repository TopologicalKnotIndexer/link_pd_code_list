# link-pd-code-list

Source data and extraction scripts for the prime-link PD-code catalogue.

## Installation

The normalized catalogue is `data/pd_code_list.txt`; scripts under `scripts/` rebuild it from source material.

## Quick start

The normalized catalogue is `data/pd_code_list.txt`; scripts under `scripts/` rebuild it from source material.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
