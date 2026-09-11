from __future__ import annotations

from core.formats import (
    BEST_AUDIO,
    BEST_VIDEO,
    build_audio_options,
    build_video_options,
    format_duration,
    human_size,
)


class TestHumanSize:
    def test_none_returns_na(self):
        assert human_size(None) == "size n/a"

    def test_zero_returns_na(self):
        assert human_size(0) == "size n/a"

    def test_bytes(self):
        assert human_size(512) == "512 B"

    def test_one_kb(self):
        assert human_size(1024) == "1.0 KB"

    def test_one_mb(self):
        assert human_size(1_048_576) == "1.0 MB"

    def test_one_gb(self):
        assert human_size(1_073_741_824) == "1.0 GB"

    def test_one_tb(self):
        assert human_size(1_099_511_627_776) == "1.0 TB"

    def test_large_value_caps_at_tb(self):
        result = human_size(5_000_000_000_000)
        assert "TB" in result


class TestFormatDuration:
    def test_none_returns_question(self):
        assert format_duration(None) == "?"

    def test_zero_returns_question(self):
        assert format_duration(0) == "?"

    def test_seconds_only(self):
        assert format_duration(45) == "0:45"

    def test_minutes_and_seconds(self):
        assert format_duration(125) == "2:05"

    def test_hours_minutes_seconds(self):
        assert format_duration(3661) == "1:01:01"

    def test_exact_hour(self):
        assert format_duration(3600) == "1:00:00"

    def test_large_duration(self):
        assert format_duration(7200) == "2:00:00"


class TestBuildVideoOptions:
    def test_returns_best_option_first(self, sample_video_formats):
        options = build_video_options(sample_video_formats)
        assert len(options) > 0
        assert options[0].value == BEST_VIDEO

    def test_deduplicates_by_resolution_and_fps(self, sample_video_formats):
        options = build_video_options(sample_video_formats)
        keys_seen = set()
        for opt in options[1:]:
            # label starts with resolution e.g. "1080p"
            assert "p" in opt.label
            # No duplicate (height, fps) combos
            assert opt.label not in keys_seen
            keys_seen.add(opt.label)

    def test_prefers_format_with_audio(self):
        formats = [
            {"format_id": "1", "vcodec": "avc1", "height": 720, "fps": 30,
             "ext": "mp4", "filesize": 30_000_000, "acodec": "none"},
            {"format_id": "2", "vcodec": "avc1", "height": 720, "fps": 30,
             "ext": "mp4", "filesize": 28_000_000, "acodec": "mp4a"},
        ]
        options = build_video_options(formats)
        # Should pick the one with audio, even though smaller
        video_opts = [o for o in options if "720p" in o.label]
        assert len(video_opts) == 1
        assert "+audio" not in video_opts[0].label

    def test_skips_audio_only_formats(self):
        formats = [
            {"format_id": "1", "vcodec": "none", "height": 0, "fps": 30,
             "ext": "mp4", "filesize": 5_000_000, "acodec": "mp4a"},
        ]
        options = build_video_options(formats)
        assert len(options) == 1  # only the "Best" option


class TestBuildAudioOptions:
    def test_returns_best_option_first(self, sample_audio_formats):
        options = build_audio_options(sample_audio_formats)
        assert len(options) > 0
        assert options[0].value == BEST_AUDIO

    def test_sorted_by_bitrate_descending(self, sample_audio_formats):
        options = build_audio_options(sample_audio_formats)
        bitrates = [int(opt.value) for opt in options[1:]]
        assert bitrates == sorted(bitrates, reverse=True)

    def test_skips_video_formats(self):
        formats = [
            {"format_id": "1", "vcodec": "avc1", "height": 720, "fps": 30,
             "ext": "mp4", "filesize": 30_000_000, "acodec": "mp4a",
             "abr": 128},
            {"format_id": "2", "vcodec": "none", "height": 0, "fps": 0,
             "ext": "m4a", "filesize": 8_000_000, "acodec": "mp4a",
             "abr": 128},
        ]
        options = build_audio_options(formats)
        # Only best + the 128kbps audio format
        assert len(options) == 2

    def test_fallback_bitrates_when_no_audio_formats(self):
        formats = [
            {"format_id": "1", "vcodec": "avc1", "height": 720, "fps": 30,
             "ext": "mp4", "filesize": 30_000_000, "acodec": "mp4a"},
        ]
        options = build_audio_options(formats)
        # best + fallback 128, 192, 320
        labels = [o.label for o in options]
        assert any("128" in lbl for lbl in labels)
        assert any("192" in lbl for lbl in labels)
        assert any("320" in lbl for lbl in labels)
