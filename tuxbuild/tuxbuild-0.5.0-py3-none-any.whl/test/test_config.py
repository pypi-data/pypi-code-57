# -*- coding: utf-8 -*-

import pytest
import requests
import tuxbuild.config
import tuxbuild.exceptions


def test_config_FileNotFoundError():
    with pytest.raises(tuxbuild.exceptions.CantGetConfiguration):
        tuxbuild.config.Config(config_path="/nonexistent")


def test_config_token_from_env(monkeypatch, sample_token):
    """ Set TUXBUILD_TOKEN in env and ensure it is used """
    monkeypatch.setenv("TUXBUILD_TOKEN", sample_token)
    c = tuxbuild.config.Config(config_path="/nonexistent")
    assert c.auth_token == sample_token
    assert c.kbapi_url == c.default_api_url
    assert c.get_auth_token() == c.auth_token
    assert c.get_kbapi_url() == c.kbapi_url
    assert c.get_tuxbuild_env() == c.tuxbuild_env


def test_config_token_and_url_from_env(monkeypatch, sample_token, sample_url):
    """ Set TUXBUILD_TOKEN in env and ensure it is used """
    monkeypatch.setenv("TUXBUILD_TOKEN", sample_token)
    monkeypatch.setenv("TUXBUILD_URL", sample_url)
    c = tuxbuild.config.Config(config_path="/nonexistent")
    assert c.auth_token == sample_token
    assert c.kbapi_url == sample_url
    assert c.get_auth_token() == c.auth_token
    assert c.get_kbapi_url() == c.kbapi_url
    assert c.get_tuxbuild_env() == c.tuxbuild_env


def test_config_file_minimum(tmp_path, sample_token):
    contents = """
[default]
token={}
""".format(
        sample_token
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    c = tuxbuild.config.Config(config_path=config_file)
    assert c.auth_token == sample_token
    assert c.kbapi_url == c.default_api_url
    assert c.get_auth_token() == c.auth_token
    assert c.get_kbapi_url() == c.kbapi_url
    assert c.get_tuxbuild_env() == c.tuxbuild_env


def test_config_file_no_token(tmp_path):
    contents = """
[default]
"""
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    with pytest.raises(tuxbuild.exceptions.TokenNotFound):
        tuxbuild.config.Config(config_path=config_file)


def test_config_file_section(tmp_path):
    config_file = tmp_path / "config.ini"
    config_file.write_text("")
    with pytest.raises(tuxbuild.exceptions.InvalidConfiguration):
        tuxbuild.config.Config(config_path=config_file)


def test_config_file_default(tmp_path, sample_token, sample_url):
    contents = """
[default]
token={}
api_url={}
""".format(
        sample_token, sample_url
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    c = tuxbuild.config.Config(config_path=config_file)
    assert c.auth_token == sample_token
    assert c.kbapi_url == sample_url
    assert c.get_auth_token() == c.auth_token
    assert c.get_kbapi_url() == c.kbapi_url
    assert c.get_tuxbuild_env() == c.tuxbuild_env


def test_config_file_non_default(monkeypatch, tmp_path, sample_token, sample_url):
    contents = """
[default]
token=foo
api_url=bar
[foobar]
token={}
api_url={}
""".format(
        sample_token, sample_url
    )
    monkeypatch.setenv("TUXBUILD_ENV", "foobar")
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    c = tuxbuild.config.Config(config_path=config_file)
    assert c.auth_token == sample_token
    assert c.kbapi_url == sample_url
    assert c.get_auth_token() == c.auth_token
    assert c.get_kbapi_url() == c.kbapi_url
    assert c.get_tuxbuild_env() == c.tuxbuild_env


def test_check_auth_token_valid(config, sample_url, get, response, mocker):
    response.status_code = 200
    config.check_auth_token()
    get.assert_called_with(f"{sample_url}/verify", headers=mocker.ANY)


def test_check_auth_token_invalid(config, sample_url, get, response):
    response.status_code = 400
    with pytest.raises(requests.HTTPError):
        config.check_auth_token()


def test_check_auth_token_retries_on_server_error(config, get, response, sleep):
    response.status_code = 500

    config.check_auth_token()
    assert get.call_count == 6
    # retries with expontential backoff
    assert sleep.called_with(1)
    assert sleep.called_with(2)
    assert sleep.called_with(4)
    assert sleep.called_with(8)
    assert sleep.called_with(16)
    assert sleep.call_count == 5
