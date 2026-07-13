"""Validate every committed normalized link PD-code record."""

from ast import literal_eval
from pathlib import Path

from extract_pdcode import validate_record


def validate_file(path: str | Path) -> int:
    source = Path(path)
    names = set()
    count = 0
    for line_number, raw_line in enumerate(
        source.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError(f"malformed record at line {line_number}")
        name, raw_pd_code = raw_line.split(":", 1)
        if name in names:
            raise ValueError(f"duplicate name at line {line_number}: {name}")
        pd_code = literal_eval(raw_pd_code)
        validate_record(name, pd_code)
        names.add(name)
        count += 1
    return count


if __name__ == "__main__":
    default = Path(__file__).resolve().parents[1] / "data" / "pd_code_list.txt"
    print(f"validated {validate_file(default)} records")
