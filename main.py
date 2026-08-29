from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from rich.panel import Panel

from core.downloader import Downloader, ffmpeg_available
from core.formats import (
    BEST_AUDIO,
    build_audio_options,
    build_video_options,
    format_duration,
    human_size,
)
from core.paths import default_save_dir, ensure_dir
from ui import prompts
from ui.banner import APP_NAME, VERSION, console, print_banner
from ui.progress import DownloadHook, create_progress

downloader = Downloader()


def check_ffmpeg() -> bool:
    if ffmpeg_available():
        console.print("[success]✓ ffmpeg detected[/] · MP3 conversion and muxing enabled")
        return True
    console.print(
        "[warning]⚠ ffmpeg not found[/] — MP3 extraction and video muxing need it."
    )
    console.print(
        "  Install it with [info]winget install ffmpeg[/]"
        " (Windows), [info]brew install ffmpeg[/] (macOS), or your package manager."
    )
    return False


def show_video_summary(info: dict[str, Any]) -> None:
    title = info.get("title", "Unknown title")
    uploader = info.get("uploader") or info.get("channel") or "Unknown channel"
    artist = info.get("artist")
    album = info.get("album")
    duration = format_duration(info.get("duration"))
    n_formats = len(info.get("formats") or [])
    lines = [
        f"[title]{title}[/]\n",
        f"[info]Channel:[/]   {uploader}",
        f"[info]Duration:[/]  {duration}",
        f"[info]Formats:[/]   {n_formats} available",
    ]
    if artist:
        lines.append(f"[info]Artist:[/]   {artist}")
    if album:
        lines.append(f"[info]Album:[/]    {album}")
    console.print(Panel("\n".join(lines), border_style="cyan", padding=(1, 2)))


def choose_save_dir() -> Path:
    while True:
        path = prompts.ask_save_dir(default_save_dir())
        if path.exists():
            return path
        if not prompts.confirm_create_dir(path):
            continue
        ensure_dir(path)
        console.print(f"[success]✓ Created folder[/] [info]{path}[/]")
        return path


def run_download(url: str, info: dict[str, Any]) -> None:
    media_type = prompts.ask_media_type()

    if media_type == "mp3":
        if not ffmpeg_available():
            console.print("[error]MP3 conversion requires ffmpeg — aborting this download.[/]")
            return
        options = build_audio_options(info.get("formats") or [])
        choice = prompts.ask_audio_bitrate(options)
        format_sel = BEST_AUDIO
        bitrate = None if choice == BEST_AUDIO else choice
    else:
        options = build_video_options(info.get("formats") or [])
        format_sel = prompts.ask_video_quality(options)
        bitrate = None

    save_dir = choose_save_dir()

    progress = create_progress()
    task_id = progress.add_task("Downloading…", total=None)
    finalize_status: Any = None

    def on_finished() -> None:
        nonlocal finalize_status
        progress.stop()
        finalize_status = console.status(
            "Finalizing file (ffmpeg — converting / merging)…"
        )
        finalize_status.start()

    hook = DownloadHook(progress, task_id, on_finished=on_finished)

    console.print("[info]Starting download…[/]")
    progress.start()
    try:
        final_path, _ = downloader.download(
            url,
            format_sel,
            save_dir,
            media_type=media_type,
            bitrate=bitrate,
            progress_hook=hook,
        )
    except Exception as exc:
        progress.stop()
        console.print(f"[error]✗ Download failed:[/] {exc}")
        return
    finally:
        if finalize_status is not None:
            finalize_status.stop()

    if not final_path.exists():
        console.print("[warning]Download completed but the final file was not found.[/]")
        return

    if media_type == "mp3":
        for ext in (".info.json", ".webp", ".jpg", ".description"):
            sidecar = final_path.with_suffix(ext)
            if sidecar.exists():
                sidecar.unlink()

    size = human_size(final_path.stat().st_size)
    artist = info.get("artist")
    album = info.get("album")
    details = (
        f"[success]✓ {final_path.name}[/]\n"
        f"[info]Size:[/]  {size}\n"
        f"[info]Path:[/]  {final_path.parent}"
    )
    if artist:
        details += f"\n[info]Artist:[/] {artist}"
    if album:
        details += f"\n[info]Album:[/]  {album}"
    console.print(
        Panel(
            details,
            title="[bold green]Download complete[/]",
            border_style="green",
            padding=(1, 2),
        )
    )


def main() -> None:
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"{APP_NAME} {VERSION}")
        return

    print_banner()
    check_ffmpeg()

    while True:
        try:
            url = prompts.ask_url()
            if not url:
                continue

            with console.status("Fetching video info…"):
                info = downloader.fetch_info(url)

            if info.get("_type") == "playlist" and info.get("entries"):
                info = info["entries"][0]

            show_video_summary(info)
            run_download(url, info)

            if not prompts.ask_download_again():
                console.print("[dim]Thanks for using YT-Down. Goodbye![/]")
                break
        except KeyboardInterrupt:
            console.print("\n[error]Aborted by user.[/]")
            break
        except Exception as exc:
            console.print(f"[error]Something went wrong:[/] {exc}")


if __name__ == "__main__":
    main()
