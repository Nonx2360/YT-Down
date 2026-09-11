from __future__ import annotations

import pytest


@pytest.fixture
def sample_video_formats():
    """Mock yt-dlp format list for video."""
    return [
        {
            "format_id": "137",
            "vcodec": "avc1",
            "height": 1080,
            "fps": 30,
            "ext": "mp4",
            "filesize": 50_000_000,
            "acodec": "none",
        },
        {
            "format_id": "248",
            "vcodec": "vp9",
            "height": 1080,
            "fps": 60,
            "ext": "webm",
            "filesize": 45_000_000,
            "acodec": "none",
        },
        {
            "format_id": "22",
            "vcodec": "avc1",
            "height": 720,
            "fps": 30,
            "ext": "mp4",
            "filesize": 30_000_000,
            "acodec": "mp4a",
        },
        {
            "format_id": "18",
            "vcodec": "avc1",
            "height": 360,
            "fps": 30,
            "ext": "mp4",
            "filesize": 10_000_000,
            "acodec": "mp4a",
        },
    ]


@pytest.fixture
def sample_audio_formats():
    """Mock yt-dlp format list for audio."""
    return [
        {
            "format_id": "251",
            "vcodec": "none",
            "acodec": "opus",
            "abr": 160,
            "ext": "webm",
            "filesize": 12_000_000,
        },
        {
            "format_id": "140",
            "vcodec": "none",
            "acodec": "mp4a",
            "abr": 128,
            "ext": "m4a",
            "filesize": 8_000_000,
        },
        {
            "format_id": "139",
            "vcodec": "none",
            "acodec": "mp4a",
            "abr": 48,
            "ext": "m4a",
            "filesize": 3_000_000,
        },
    ]
