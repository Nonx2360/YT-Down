# YT-Down — YouTube Downloader CLI

A colorful, interactive terminal tool to download YouTube videos as **MP4** or **MP3**, with
quality selection and a custom save location.

![flow](docs/flow.png)

## Features

- Interactive arrow-key menus (no typing numbers)
- MP4 download with every available resolution picked dynamically from the video (144p → 4K, incl. 60fps)
- MP3 extraction with bitrate choice (128 / 192 / 320 kbps, or best)
- Embedded metadata on MP3s — title, artist, album, genre, date, description, and album art thumbnail
- Live progress bar with percent, speed, and ETA
- Rich colored panels, banner, and error handling (no raw tracebacks)
- Custom save folder (defaults to `~/Downloads/yt-cli/`, auto-created)
- Downloads one video at a time; loop until you quit

## Requirements

- Python 3.9+
- `ffmpeg` on your PATH (needed for MP3 conversion and video muxing)

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

```bash
python main.py
```

Then follow the prompts: paste a URL → pick MP4/MP3 → pick quality → pick save folder → watch
the progress bar. Files are saved as `Title [video-id].mp4` / `.mp3`.

## Troubleshooting

- **"Download failed" / extraction errors** — YouTube changes frequently; run `pip install -U yt-dlp`.
- **ffmpeg warning at startup** — install ffmpeg (see above); MP4 downloads of combined
  formats will still work, but MP3 conversion won't.

## Legal note

Only download content you have the rights to use — respect copyright and YouTube's Terms of Service.
