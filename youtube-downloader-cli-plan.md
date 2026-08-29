# YouTube Downloader CLI — Project Plan

A colorful, interactive command-line tool to download YouTube videos as MP3 or MP4, with quality selection and custom save location.

---

## 1. Goal

Build a Python CLI tool that:
- Downloads YouTube videos as **MP4** (video) or **MP3** (audio only)
- Lets the user pick from **all available qualities/formats**
- Lets the user choose **where to save** the file
- Has a **colorful, polished terminal UI** (not just plain print statements)

---

## 2. Tech Stack

| Purpose | Library | Notes |
|---|---|---|
| Download engine | `yt-dlp` | Actively maintained fork of youtube-dl, handles format extraction reliably |
| Colorful CLI / UI | `rich` | Progress bars, tables, panels, colored text — best-in-class for pretty terminals |
| Interactive prompts | `questionary` (or `InquirerPy`) | Arrow-key menus for choosing format/quality/save path, feels much nicer than typing numbers |
| Audio conversion | `ffmpeg` (external binary, called via yt-dlp) | Needed for MP3 extraction — must be installed on system and in PATH |
| Path handling | `pathlib` | Cross-platform save paths |
| Packaging (optional) | `pyinstaller` or `pipx` | To ship as a standalone executable later |

Install core deps:
```bash
pip install yt-dlp rich questionary
```
User also needs `ffmpeg` installed separately (not a pip package).

---

## 3. Core User Flow

1. **Welcome banner** (rich `Panel`/ASCII art with color)
2. **Prompt: paste YouTube URL**
3. **Fetch video info** via `yt-dlp` (title, duration, thumbnail-in-text, available formats) — show a spinner while fetching
4. **Prompt: choose type** → `MP4 (video)` or `MP3 (audio only)`
5. **Prompt: choose quality**
   - If MP4 → list all available resolutions/formats (e.g. 144p, 360p, 720p, 1080p, 4K if available) pulled dynamically from `yt-dlp`'s format list, not hardcoded
   - If MP3 → list available audio bitrates (e.g. 128kbps, 192kbps, 320kbps)
6. **Prompt: choose save folder** (default suggestion + option to type custom path, validate it exists or offer to create it)
7. **Download with live progress bar** (rich `Progress`) showing % , speed, ETA
8. **Success summary panel** — file name, size, save path, done in colored box
9. Loop back to "download another?" or exit

---

## 4. Project Structure

```
yt-cli/
├── main.py                # Entry point, orchestrates the flow
├── core/
│   ├── downloader.py       # Wraps yt-dlp calls (fetch info, list formats, download)
│   ├── formats.py          # Parses/filters yt-dlp format list into clean MP4/MP3 options
│   └── paths.py             # Save-location handling & validation
├── ui/
│   ├── banner.py            # Startup banner / styling constants (rich Theme)
│   ├── prompts.py           # All questionary interactive prompts
│   └── progress.py          # Rich progress bar hook for yt-dlp's progress_hooks
├── requirements.txt
└── README.md
```

---

## 5. Key Implementation Notes

- **Getting available qualities dynamically**: use `yt_dlp.YoutubeDL().extract_info(url, download=False)` and read the `formats` list — filter for video-only/audio-only/combined streams, dedupe by resolution/bitrate, and label them nicely (e.g. "1080p60 · mp4 · 45MB").
- **MP3 extraction**: use yt-dlp's `postprocessors` option with `FFmpegExtractAudio`, setting `preferredquality` to the bitrate the user picked.
- **Progress bar hookup**: yt-dlp supports a `progress_hooks` callback — feed the `downloaded_bytes`/`total_bytes` into a `rich.progress.Progress` instance for a live bar.
- **Color theme**: define a consistent `rich.theme.Theme` (e.g. cyan for prompts, green for success, red for errors, yellow for warnings) so the whole app feels cohesive instead of random colors.
- **Save path**: default to `~/Downloads/yt-cli/`, auto-create if missing, but always let the user override.
- **Error handling**: wrap downloads in try/except for invalid URLs, age-restricted/private videos, no ffmpeg found, no internet — show clean red error panels instead of raw tracebacks.
- **Filename sanitization**: strip illegal characters from video titles before saving.

---

## 6. Stretch Features (Optional, Later)

- Playlist support (download all / select videos from a playlist)
- Download history log (rich table of past downloads)
- Config file (`config.toml`) to remember default save folder & preferred quality
- Batch mode: paste multiple URLs at once
- Subtitle download option (`.srt`)
- Thumbnail embedding into MP3 (album art) via ffmpeg ✓ DONE
- Embedded metadata on MP3s (title, artist, album, genre, date, description, album art) via ffmpeg ✓ DONE
- Simple `--url` CLI flag mode for non-interactive/scripted use (alongside interactive mode)

---

## 7. Build Order (Milestones)

1. ✅ Basic yt-dlp download working from hardcoded URL (no UI)
2. ✅ Add format listing + let user pick quality via plain input
3. ✅ Swap plain input for `questionary` interactive menus
4. ✅ Add `rich` banner, colored panels, and progress bar
5. ✅ Add MP3 extraction path with ffmpeg
6. ✅ Add custom save location logic + validation
7. ✅ Polish error handling and edge cases
8. ⬜ (Optional) Package with pyinstaller for a standalone `.exe`/binary

---

## 8. Notes / Caveats

- Requires `ffmpeg` installed and on PATH — plan should include an install-check on startup that gives a friendly message if missing.
- YouTube changes their site frequently; `yt-dlp` needs to be kept updated (`pip install -U yt-dlp`) to keep working.
- For personal/freelance distribution, worth adding a short note in the README about only downloading content you have rights to use.