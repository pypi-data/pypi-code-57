# -*- coding: utf-8 -*-

import requests as requests_orig
import tuxbuild.config
import pytest


@pytest.fixture(autouse=True)
def requests(mocker):
    """
    Disables any real HTTP requests completely. This avoids the test suite
    hitting the network for real.
    """
    mocker.patch("requests.delete")
    mocker.patch("requests.get")
    mocker.patch("requests.head")
    mocker.patch("requests.post")
    mocker.patch("requests.put")
    return requests_orig


@pytest.fixture
def response(requests):
    r = requests.Response()
    r.status_code = 200
    return r


@pytest.fixture
def post(requests, response):
    requests.post.return_value = response
    return requests.post


@pytest.fixture
def get(requests, response):
    requests.get.return_value = response
    return requests.get


@pytest.fixture
def sleep(mocker):
    return mocker.patch("time.sleep")


@pytest.fixture
def sample_token():
    return "Q9qMlmkjkIuIGmEAw-Mf53i_qoJ8Z2eGYCmrNx16ZLLQGrXAHRiN2ce5DGlAebOmnJFp9Ggcq9l6quZdDTtrkw"


@pytest.fixture
def sample_url():
    return "https://foo.bar.tuxbuild.com/v1"


@pytest.fixture
def config(monkeypatch, sample_token, sample_url):
    monkeypatch.setenv("TUXBUILD_TOKEN", sample_token)
    monkeypatch.setenv("TUXBUILD_URL", sample_url)
    config = tuxbuild.config.Config("/dev/null")
    config.kbapi_url = sample_url
    config.auth_token = sample_token
    return config


@pytest.fixture
def config_valid_token(config, mocker):
    mocker.patch("tuxbuild.config.Config.check_auth_token")
    return config


@pytest.fixture
def config_invalid_token(config, mocker):
    mocker.patch(
        "tuxbuild.config.Config.check_auth_token", side_effect=RuntimeError("BOOM")
    )
    return config
