from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BEST_VIDEO = "bestvideo+bestaudio/best"
BEST_AUDIO = "bestaudio/best"

FALLBACK_MP3_BITRATES = ("128", "192", "320")


@dataclass(frozen=True)
class FormatOption:
    label: str
    value: str


def human_size(num: float | int | None) -> str:
    if not num:
        return "size n/a"
    size = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} B" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return "?"


def format_duration(seconds: float | int | None) -> str:
    if not seconds:
        return "?"
    total = int(seconds)
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _filesize(f: dict[str, Any]) -> float:
    return float(f.get("filesize") or f.get("filesize_approx") or 0)


def build_video_options(formats: list[dict[str, Any]]) -> list[FormatOption]:
    """Collapse the raw yt-dlp format list into one option per resolution/fps."""
    best: dict[tuple[int, int], dict[str, Any]] = {}
    for f in formats:
        vcodec = f.get("vcodec") or "none"
        if vcodec == "none":
            continue
        height = f.get("height") or 0
        if height <= 0:
            continue
        fps = f.get("fps") or 30
        key = (height, fps)
        current = best.get(key)
        if current is None:
            best[key] = f
            continue
        cur_has_audio = (current.get("acodec") or "none") != "none"
        new_has_audio = (f.get("acodec") or "none") != "none"
        if new_has_audio and not cur_has_audio:
            best[key] = f
        elif new_has_audio == cur_has_audio and _filesize(f) > _filesize(current):
            best[key] = f

    options = [FormatOption("Best quality (video + audio, auto)", BEST_VIDEO)]
    for (height, fps), f in sorted(best.items(), reverse=True):
        ext = f.get("ext") or "mp4"
        size = human_size(f.get("filesize") or f.get("filesize_approx"))
        label = f"{height}p"
        if fps >= 50:
            label += str(fps)
        label += f" · {ext} · {size}"
        has_audio = (f.get("acodec") or "none") != "none"
        if not has_audio:
            label += " · +audio (muxed)"
            value = f"{f['format_id']}+bestaudio/best"
        else:
            value = f["format_id"]
        options.append(FormatOption(label, value))
    return options


def build_audio_options(formats: list[dict[str, Any]]) -> list[FormatOption]:
    """Collapse audio-only formats into one option per available bitrate."""
    best: dict[int, dict[str, Any]] = {}
    for f in formats:
        vcodec = f.get("vcodec") or "none"
        if vcodec != "none":
            continue
        acodec = f.get("acodec") or "none"
        if acodec == "none":
            continue
        bitrate = int(round(f.get("abr") or 0))
        if bitrate <= 0:
            continue
        current = best.get(bitrate)
        if current is None or _filesize(f) > _filesize(current):
            best[bitrate] = f

    options = [FormatOption("Best quality (highest bitrate available)", BEST_AUDIO)]
    for bitrate, f in sorted(best.items(), reverse=True):
        ext = f.get("ext") or "?"
        size = human_size(f.get("filesize") or f.get("filesize_approx"))
        options.append(FormatOption(f"{bitrate} kbps · {ext} · {size}", str(bitrate)))

    if not best:
        for b in FALLBACK_MP3_BITRATES:
            options.append(FormatOption(f"{b} kbps", b))
    return options
