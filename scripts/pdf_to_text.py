"""Convert a PDF to UTF-8 text with Poppler's pdftotext executable."""

from argparse import ArgumentParser
from pathlib import Path
import shutil
import subprocess


def pdf_to_text(pdf_path: str, text_path: str | None = None) -> str:
    source = Path(pdf_path)
    if not source.is_file():
        raise FileNotFoundError(source)
    destination = Path(text_path) if text_path else source.with_suffix(".txt")
    executable = shutil.which("pdftotext")
    if executable is None:
        raise FileNotFoundError("pdftotext is not on PATH")
    result = subprocess.run(
        [executable, "-enc", "UTF-8", str(source), str(destination)],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"pdftotext exited {result.returncode}")
    return str(destination)


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_pdf")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    output = pdf_to_text(args.input_pdf, args.output)
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
