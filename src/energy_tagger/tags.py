from __future__ import annotations

from mutagen import File
from mutagen.id3 import ID3, COMM, TIT1, ID3NoHeaderError


def update_tag(path: str, energy: int, field: str) -> None:
    """
    Write the computed energy score into the requested tag field.

    field:
      - "comment"
      - "grouping"
    """
    energy_str = f"Energy {energy}"

    try:
        if path.lower().endswith(".mp3"):
            try:
                tags = ID3(path)
            except ID3NoHeaderError:
                tags = ID3()

            if field == "comment":
                tags.delall("COMM")
                tags.add(COMM(encoding=3, lang="eng", desc="", text=energy_str))
            elif field == "grouping":
                tags.delall("TIT1")
                tags.add(TIT1(encoding=3, text=energy_str))
            else:
                raise ValueError(f"Unsupported field: {field}")

            tags.save(path)
            print(f"[WRITE] {path} -> {energy_str}")
            return

        if path.lower().endswith(".flac"):
            audio = File(path, easy=False)

            if audio is None:
                print(f"[SKIP] Unsupported: {path}")
                return

            if field == "comment":
                audio["comment"] = [energy_str]
            elif field == "grouping":
                audio["grouping"] = [energy_str]
            else:
                raise ValueError(f"Unsupported field: {field}")

            audio.save()
            print(f"[WRITE] {path} -> {energy_str}")
            return

        print(f"[SKIP] Unsupported extension: {path}")

    except Exception as exc:
        print(f"[ERROR] Writing {path}: {exc}")
