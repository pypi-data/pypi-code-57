from pathlib import Path

from modelzoo import auth, config


def test_save_api_key(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("builtins.input", lambda x: "test-api-key")
    assert auth() == "test-api-key"


def test_config_priority(monkeypatch, tmp_path):
    # Lowest priority: config file. If the file doesn't exist, the user will be
    # prompted for it.
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("builtins.input", lambda x: "test-api-key")
    assert config.get_api_key() == "test-api-key"

    # Second priority: environment variable.
    monkeypatch.setenv(config.CONFIG_API_KEY_ENV_VAR, "test-api-key-2")
    assert config.get_api_key() == "test-api-key-2"

    # Highest priority: environment variable
    assert config.get_api_key("test-api-key-3") == "test-api-key-3"
