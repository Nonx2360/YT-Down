from __future__ import annotations

import argparse

from core.config import Config


def parse_args(config: Config) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="yt-down",
        description="Interactive YouTube downloader CLI",
    )
    parser.add_argument("--version", "-V", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("--url", "-u", help="YouTube URL (skips interactive prompt)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["mp4", "mp3"],
        default=config.default_format,
        help=f"Media format (default: {config.default_format})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output directory (overrides config)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=str,
        default=config.default_quality,
        help="Quality preset (e.g. 720, 128) or 'best'",
    )
    parser.add_argument(
        "--yes-playlist",
        action="store_true",
        default=config.yes_playlist,
        help="Download all playlist entries without prompting",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show debug output")
    return parser.parse_args()
