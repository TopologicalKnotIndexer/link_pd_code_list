"""Delete non-hidden, empty regular files below an explicitly selected folder."""

from argparse import ArgumentParser
from pathlib import Path


def delete_empty_files(target_dir: str | Path) -> list[Path]:
    root = Path(target_dir).resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    deleted = []
    for path in sorted(root.rglob("*")):
        if path.name.startswith(".") or path.is_symlink() or not path.is_file():
            continue
        if not path.read_bytes().strip():
            path.unlink()
            deleted.append(path)
    return deleted


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    args = parser.parse_args()
    for path in delete_empty_files(args.directory):
        print(f"deleted: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
