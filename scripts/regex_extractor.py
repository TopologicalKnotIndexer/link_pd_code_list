"""Extract unique Knot Atlas link-table URLs from an HTML document."""

from argparse import ArgumentParser
from pathlib import Path
import re


LINK_PATH = re.compile(r'"(?P<path>/wiki/L\d+(?:a|n)\d+)"')


def extract_patterns(file_path: str | Path) -> list[str]:
    source = Path(file_path)
    text = source.read_text(encoding="utf-8-sig")
    return sorted({match.group("path") for match in LINK_PATH.finditer(text)})


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()
    urls = ["https://katlas.org" + path for path in extract_patterns(args.input_path)]
    Path(args.output_path).write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"extracted {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
