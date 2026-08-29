from __future__ import annotations

from pathlib import Path

DEFAULT_SAVE_DIR = Path.home() / "Downloads" / "yt-cli"


def default_save_dir() -> Path:
    return DEFAULT_SAVE_DIR


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
