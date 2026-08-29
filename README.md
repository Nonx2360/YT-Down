# YT-Down — YouTube Downloader CLI

<p align="center">
  <img src="logo.png" alt="YT-Down Logo" width="400">
</p>

A colorful, interactive terminal tool to download YouTube videos as **MP4** or **MP3**, with
quality selection, custom save location, and full song metadata.

<p align="center">
  <img src="usecase.png" alt="YT-Down in action" width="700">
</p>

## Features

- Interactive arrow-key menus (no typing numbers)
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

- Python 3.9+
- `ffmpeg` on your PATH (needed for MP3 conversion, metadata embedding, and video muxing)

## Install

```bash
pip install -r requirements.txt
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

### From source

```bash
python main.py
```

### Standalone exe

Download `YT-Down.exe` from the `dist/` folder (or build it yourself):

```bash
python -m PyInstaller --clean YT-Down.spec
```

Then follow the prompts: paste a URL → pick MP4/MP3 → pick quality → pick save folder → watch
the progress bar. Files are saved as `Title [video-id].mp4` / `.mp3`.

## Building the exe

```bash
pip install pyinstaller
python -m PyInstaller --clean YT-Down.spec
```

The output is `dist/YT-Down.exe`.

## Troubleshooting

- **"Download failed" / extraction errors** — YouTube changes frequently; run `pip install -U yt-dlp`.
- **ffmpeg warning at startup** — install ffmpeg (see above); MP4 downloads of combined
  formats will still work, but MP3 conversion and metadata embedding won't.
- **exe won't start** — make sure `ffmpeg` is installed and on your PATH.

## Legal note

Only download content you have the rights to use — respect copyright and YouTube's Terms of Service.
