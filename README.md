# YT-Down — YouTube Downloader CLI

<p align="center">
  <img src="logo.png" alt="YT-Down Logo" width="400">
</p>

A colorful, interactive terminal tool to download YouTube videos as **MP4** or **MP3**, with
quality selection, custom save location, full song metadata, and playlist support.

<p align="center">
  <img src="usecase.png" alt="YT-Down in action" width="700">
</p>

## Features

- Interactive arrow-key menus (no typing numbers)
- **Playlist support** — download all videos or pick individual ones
- **Non-interactive CLI mode** — scriptable with `--url`, `--format`, `--output` flags
- **URL validation** — friendly errors for invalid or non-YouTube links
- **Resume support** — interrupted downloads pick up where they left off
- **Config file** — persist your preferred save dir and format in `~/.config/yt-down/config.toml`
- **Thumbnail preview** — see the video thumbnail in your terminal before downloading
- MP4 download with every available resolution picked dynamically from the video (144p → 4K, incl. 60fps)
- MP3 extraction with bitrate choice (128 / 192 / 320 kbps, or best)
- Embedded metadata on MP3s — title, artist, album, genre, date, description, and album art thumbnail
- Live progress bar with percent, speed, and ETA
- Rich colored panels, banner, and error handling (no raw tracebacks)
- Custom save folder (defaults to `~/Downloads/yt-cli/`, auto-created)
- Standalone `.exe` available (no Python install needed)
- Downloads one video at a time; loop until you quit

## Requirements

- Python 3.10+
- `ffmpeg` on your PATH (needed for MP3 conversion, metadata embedding, and video muxing)

## Install

```bash
pip install -e .
```

Or with development dependencies (pytest, ruff):

```bash
pip install -e ".[dev]"
```

Install ffmpeg (if missing):

```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Debian/Ubuntu
sudo apt install ffmpeg
```

## Usage

### Interactive mode (default)

```bash
yt-down
```

Or from source:

```bash
python main.py
```

Follow the prompts: paste a URL → pick MP4/MP3 → pick quality → pick save folder → watch
the progress bar. Files are saved as `Title [video-id].mp4` / `.mp3`.

### Non-interactive mode

Run directly from the command line without prompts:

```bash
yt-down --url "https://youtube.com/watch?v=..." --format mp4 --output ~/Videos
```

#### CLI flags

| Flag | Description |
|------|-------------|
| `--url`, `-u` | YouTube URL (skips all interactive prompts) |
| `--format`, `-f` | `mp4` or `mp3` (default: `mp4`) |
| `--output`, `-o` | Output directory |
| `--quality`, `-q` | Quality preset (e.g. `720`, `128`) or `best` |
| `--yes-playlist` | Download all playlist entries without prompting |
| `--verbose`, `-v` | Show debug output (client fallback info) |
| `--version`, `-V` | Show version |

### Playlist handling

When a playlist URL is detected, you'll be prompted to:

- **Download all** — iterates through every video in the playlist
- **Download first** — grabs only the first entry
- **Cancel**

Use `--yes-playlist` to auto-download all entries without prompting.

### Configuration file

Create `~/.config/yt-down/config.toml` to persist defaults:

```toml
save_dir = "~/Videos"
default_format = "mp3"
title_max_chars = 80
yes_playlist = true
```

CLI flags always override config file values.

## Building the exe

```bash
pip install pyinstaller
python -m PyInstaller --clean YT-Down.spec
```

The output is `dist/YT-Down.exe`.

## Development

```bash
pip install -e ".[dev]"
ruff check .        # lint
pytest              # run tests
```

## Troubleshooting

- **"Download failed" / extraction errors** — YouTube changes frequently; run `pip install -U yt-dlp`.
- **ffmpeg warning at startup** — install ffmpeg (see above); MP4 downloads of combined
  formats will still work, but MP3 conversion and metadata embedding won't.
- **exe won't start** — make sure `ffmpeg` is installed and on your PATH.
- **Use `--verbose`** — shows which YouTube client fallback succeeded, useful for debugging.

## Legal note

Only download content you have the rights to use — respect copyright and YouTube's Terms of Service.
