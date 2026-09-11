from __future__ import annotations

from pathlib import Path

from core.paths import DEFAULT_SAVE_DIR, default_save_dir, ensure_dir


class TestDefaultSaveDir:
    def test_returns_home_downloads_yt_cli(self):
        result = default_save_dir()
        assert result == Path.home() / "Downloads" / "yt-cli"

    def test_constant_matches_function(self):
        assert default_save_dir() == DEFAULT_SAVE_DIR


class TestEnsureDir:
    def test_creates_directory(self, tmp_path):
        target = tmp_path / "sub1" / "sub2"
        result = ensure_dir(target)
        assert result == target
        assert target.is_dir()

    def test_idempotent(self, tmp_path):
        target = tmp_path / "exists"
        target.mkdir()
        result = ensure_dir(target)
        assert result == target
        assert target.is_dir()
