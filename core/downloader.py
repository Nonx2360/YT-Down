from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp

ProgressHook = Callable[[dict[str, Any]], None]

CLIENT_FALLBACKS: tuple[str | None, ...] = (None, "android", "tv", "ios")


class _SilentLogger:
    def debug(self, msg: str) -> None:
        pass

    def info(self, msg: str) -> None:
        pass

    def warning(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass


SILENT_LOGGER = _SilentLogger()


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


class Downloader:
    def fetch_info(self, url: str) -> dict[str, Any]:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "logger": SILENT_LOGGER,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)

    def download(
        self,
        url: str,
        format_sel: str,
        save_dir: Path,
        media_type: str = "mp4",
        bitrate: Optional[str] = None,
        progress_hook: Optional[ProgressHook] = None,
    ) -> tuple[Path, str]:
        postprocessors: list[dict[str, Any]] = []
        if media_type == "mp3":
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate or "0",
                }
            )
            postprocessors.append({"key": "FFmpegMetadata"})
            postprocessors.append({"key": "EmbedThumbnail"})

        save_dir.mkdir(parents=True, exist_ok=True)
        outtmpl = str(save_dir / "%(title).120B [%(id)s].%(ext)s")

        info: Optional[dict[str, Any]] = None
        last_error: Optional[Exception] = None
        for client in CLIENT_FALLBACKS:
            opts: dict[str, Any] = {
                "format": format_sel,
                "outtmpl": outtmpl,
                "quiet": True,
                "no_warnings": True,
                "noprogress": True,
                "noplaylist": True,
                "logger": SILENT_LOGGER,
                "progress_hooks": [progress_hook] if progress_hook else [],
                "postprocessors": postprocessors,
                "merge_output_format": "mp4",
                "writethumbnail": media_type == "mp3",
                "writeinfojson": media_type == "mp3",
            }
            if client is not None:
                opts["extractor_args"] = {
                    "youtube": {"player_client": [client]}
                }
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                break
            except Exception as exc:
                last_error = exc
                continue

        if info is None:
            raise last_error or RuntimeError("Download failed for an unknown reason.")

        title = info.get("title", "video")
        requested = info.get("requested_downloads") or [{}]
        filepath = requested[0].get("filepath") or info.get("filepath")
        if not filepath:
            raise RuntimeError("Could not determine the downloaded file path.")
        final = Path(filepath)
        if media_type == "mp3":
            final = final.with_suffix(".mp3")
        return final, title
