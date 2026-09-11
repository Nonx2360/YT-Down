from __future__ import annotations

from core.validation import validate_youtube_url


class TestValidateYoutubeUrl:
    def test_valid_watch_url(self):
        valid, url = validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert valid is True
        assert url.startswith("https://")

    def test_valid_short_url(self):
        valid, url = validate_youtube_url("https://youtu.be/dQw4w9WgXcQ")
        assert valid is True

    def test_valid_music_url(self):
        valid, url = validate_youtube_url(
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        assert valid is True

    def test_valid_shorts_url(self):
        valid, url = validate_youtube_url(
            "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        )
        assert valid is True

    def test_valid_playlist_url(self):
        valid, url = validate_youtube_url(
            "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
        )
        assert valid is True

    def test_valid_embed_url(self):
        valid, url = validate_youtube_url(
            "https://www.youtube.com/embed/dQw4w9WgXcQ"
        )
        assert valid is True

    def test_no_scheme_adds_https(self):
        valid, url = validate_youtube_url("www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert valid is True
        assert url.startswith("https://")

    def test_http_upgraded_to_https(self):
        valid, url = validate_youtube_url("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert valid is True
        assert url.startswith("https://")

    def test_empty_string_invalid(self):
        valid, msg = validate_youtube_url("")
        assert valid is False
        assert "empty" in msg.lower()

    def test_whitespace_only_invalid(self):
        valid, msg = validate_youtube_url("   ")
        assert valid is False

    def test_non_youtube_url_invalid(self):
        valid, msg = validate_youtube_url("https://vimeo.com/12345")
        assert valid is False
        assert "Not a valid YouTube URL" in msg

    def test_garbage_input_invalid(self):
        valid, msg = validate_youtube_url("not-a-url")
        assert valid is False

    def test_mobile_url(self):
        valid, url = validate_youtube_url(
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        assert valid is True
