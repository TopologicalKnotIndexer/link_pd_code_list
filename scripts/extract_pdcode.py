"""Extract one validated PD code from each tabulated-link text page."""

from argparse import ArgumentParser
from ast import literal_eval
from collections import Counter
from pathlib import Path
import re


PD_BLOCK = re.compile(r"((?:X\s*[\d,\s]+)+)", re.DOTALL)
LINK_NAME = re.compile(r"L(?P<crossings>\d+)[an]\d+")


def process_pdcode(text: str) -> list[list[int]]:
    crossings = []
    for raw_item in text.split("X"):
        item = re.sub(r"\s", "", raw_item)
        if not item:
            continue
        if "," in item:
            parts = item.split(",")
        elif len(item) == 4 and item.isdigit():
            parts = list(item)
        else:
            raise ValueError(f"ambiguous crossing encoding: {item!r}")
        if len(parts) != 4 or any(not part.isdigit() for part in parts):
            raise ValueError(f"crossing must contain four positive labels: {item!r}")
        crossings.append([int(part) for part in parts])
    return crossings


def validate_record(name: str, pd_code: list[list[int]]) -> None:
    match = LINK_NAME.fullmatch(name)
    if match is None:
        raise ValueError(f"invalid tabulated-link name: {name!r}")
    crossing_count = int(match.group("crossings"))
    if len(pd_code) != crossing_count:
        raise ValueError(
            f"{name} declares {crossing_count} crossings but contains {len(pd_code)}"
        )
    counts = Counter(label for crossing in pd_code for label in crossing)
    expected = set(range(1, 2 * crossing_count + 1))
    if set(counts) != expected or any(count != 2 for count in counts.values()):
        raise ValueError(f"{name} labels must be 1..2n and occur exactly twice")


def extract_folder(input_folder: str | Path) -> list[tuple[str, list[list[int]]]]:
    folder = Path(input_folder)
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    records = []
    names = set()
    for path in sorted(folder.glob("L*.txt"), key=lambda item: item.name):
        matches = list(PD_BLOCK.finditer(path.read_text(encoding="utf-8-sig")))
        if len(matches) != 1:
            raise ValueError(f"expected one PD block in {path}, found {len(matches)}")
        name = path.stem
        pd_code = process_pdcode(matches[0].group(0))
        validate_record(name, pd_code)
        if name in names:
            raise ValueError(f"duplicate link name: {name}")
        names.add(name)
        records.append((name, pd_code))
    return records


def write_records(records: list[tuple[str, list[list[int]]]], output_file: str | Path):
    output = Path(output_file)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(
        "".join(f"{name}:{pd_code}\n" for name, pd_code in records),
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(output)


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_folder")
    parser.add_argument("output_file")
    args = parser.parse_args()
    records = extract_folder(args.input_folder)
    write_records(records, args.output_file)
    print(f"extracted {len(records)} tabulated links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
