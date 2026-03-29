from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import compute_energy_score
from .tags import update_tag

SUPPORTED_EXTENSIONS = (".mp3", ".flac")


def iter_audio_files(path: str, recursive: bool):
    p = Path(path)

    if p.is_file():
        if p.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield str(p)
        return

    if not p.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if recursive:
        for file_path in p.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield str(file_path)
    else:
        for file_path in p.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield str(file_path)


def process_file(path: str, field: str, dry_run: bool) -> None:
    energy = compute_energy_score(path)
    if energy is None:
        return

    if dry_run:
        print(f"[DRY] {path} -> Energy {energy}")
        return

    update_tag(path, energy, field)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze MP3/FLAC files and write an energy score."
    )
    parser.add_argument("path", help="Path to a file or directory")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively",
    )
    parser.add_argument(
        "--field",
        choices=["comment", "grouping"],
        default="comment",
        help="Target metadata field",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze files without writing tags",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        found_any = False
        for file_path in iter_audio_files(args.path, args.recursive):
            found_any = True
            process_file(file_path, args.field, args.dry_run)

        if not found_any:
            print("[INFO] No supported audio files found.")

    except Exception as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
