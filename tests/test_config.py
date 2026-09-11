from __future__ import annotations

from pathlib import Path

from core.config import Config, load_config


class TestConfig:
    def test_defaults(self):
        cfg = Config()
        assert cfg.save_dir == Path.home() / "Downloads" / "yt-cli"
        assert cfg.default_format == "mp4"
        assert cfg.default_quality is None
        assert cfg.title_max_chars == 120
        assert cfg.yes_playlist is False


class TestLoadConfig:
    def test_returns_defaults_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("core.config.CONFIG_FILE", tmp_path / "nonexistent.toml")
        cfg = load_config()
        assert cfg.save_dir == Path.home() / "Downloads" / "yt-cli"
        assert cfg.default_format == "mp4"

    def test_loads_valid_toml(self, tmp_path, monkeypatch):
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            'save_dir = "~/Videos"\n'
            'default_format = "mp3"\n'
            "title_max_chars = 80\n"
            "yes_playlist = true\n"
        )
        monkeypatch.setattr("core.config.CONFIG_FILE", config_file)
        cfg = load_config()
        assert cfg.save_dir == Path("~/Videos").expanduser()
        assert cfg.default_format == "mp3"
        assert cfg.title_max_chars == 80
        assert cfg.yes_playlist is True

    def test_falls_back_on_malformed(self, tmp_path, monkeypatch):
        config_file = tmp_path / "config.toml"
        config_file.write_text("this is not valid toml {{{")
        monkeypatch.setattr("core.config.CONFIG_FILE", config_file)
        cfg = load_config()
        # Should fall back to defaults
        assert cfg.default_format == "mp4"
