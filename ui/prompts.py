from __future__ import annotations

from pathlib import Path

import questionary

from core.formats import FormatOption

STYLE = questionary.Style.from_dict(
    {
        "questionmark": "fg:ansicyan bold",
        "selected": "fg:black bg:ansigreen",
        "pointer": "fg:ansigreen bold",
        "answer": "fg:ansigreen bold",
        "instruction": "fg:ansibrightblack",
        "text": "fg:ansicyan",
        "highlighted": "fg:ansiyellow bold",
        "disabled": "fg:ansibrightblack",
    }
)

TYPE_CHOICES = [
    questionary.Choice("MP4 · Video (with audio)", value="mp4"),
    questionary.Choice("MP3 · Audio only", value="mp3"),
]


def ask_url() -> str:
    url = questionary.text(
        "Paste the YouTube URL:",
        style=STYLE,
        validate=lambda value: bool(value.strip()),
    ).ask()
    return url.strip()


def ask_media_type() -> str:
    return questionary.select(
        "What do you want to download?",
        choices=TYPE_CHOICES,
        style=STYLE,
    ).ask()


def ask_video_quality(options: list[FormatOption]) -> str:
    choices = [questionary.Choice(opt.label, value=opt.value) for opt in options]
    return questionary.select(
        "Choose video quality:",
        choices=choices,
        style=STYLE,
    ).ask()


def ask_audio_bitrate(options: list[FormatOption]) -> str:
    choices = [questionary.Choice(opt.label, value=opt.value) for opt in options]
    return questionary.select(
        "Choose MP3 bitrate:",
        choices=choices,
        style=STYLE,
    ).ask()


def ask_save_dir(default: Path) -> Path:
    answer = questionary.path(
        "Where should the file be saved?",
        default=str(default),
        style=STYLE,
        validate=lambda value: bool(value.strip()),
    ).ask()
    return Path(answer).expanduser()


def confirm_create_dir(path: Path) -> bool:
    return questionary.confirm(
        f"'{path}' doesn't exist. Create it?",
        default=True,
        style=STYLE,
    ).ask()


def ask_download_again() -> bool:
    return questionary.confirm(
        "Download another video?",
        default=True,
        style=STYLE,
    ).ask()
