from __future__ import annotations

import re

_YT_PATTERN = re.compile(
    r"^(?:https?://)?"
    r"(?:www\.|m\.)?"
    r"(?:"
    r"youtube\.com/(?:watch\?v=|playlist\?list=|shorts/|embed/)|"
    r"youtu\.be/|"
    r"music\.youtube\.com/(?:watch\?v=|playlist\?list=)"
    r")"
    r"[\w\-]+",
    re.IGNORECASE,
)


def validate_youtube_url(url: str) -> tuple[bool, str]:
    """Validate a YouTube URL.

    Returns (is_valid, cleaned_url_or_error_message).
    """
    url = url.strip()
    if not url:
        return False, "URL cannot be empty."
    if not _YT_PATTERN.match(url):
        return False, "Not a valid YouTube URL."
    if url.startswith("http://"):
        url = "https://" + url[7:]
    elif not url.startswith("https://"):
        url = "https://" + url
    return True, url
