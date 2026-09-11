from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

CONFIG_DIR = Path.home() / ".config" / "yt-down"
CONFIG_FILE = CONFIG_DIR / "config.toml"


@dataclass
class Config:
    save_dir: Path = field(default_factory=lambda: Path.home() / "Downloads" / "yt-cli")
    default_format: str = "mp4"
    default_quality: str | None = None
    title_max_chars: int = 120
    yes_playlist: bool = False


def load_config() -> Config:
    """Load config from TOML file, falling back to defaults."""
    cfg = Config()
    if not CONFIG_FILE.exists():
        return cfg
    try:
        with open(CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
        if "save_dir" in data:
            cfg.save_dir = Path(data["save_dir"]).expanduser()
        if "default_format" in data:
            cfg.default_format = data["default_format"]
        if "default_quality" in data:
            cfg.default_quality = data["default_quality"]
        if "title_max_chars" in data:
            cfg.title_max_chars = int(data["title_max_chars"])
        if "yes_playlist" in data:
            cfg.yes_playlist = bool(data["yes_playlist"])
    except Exception:
        pass
    return cfg
