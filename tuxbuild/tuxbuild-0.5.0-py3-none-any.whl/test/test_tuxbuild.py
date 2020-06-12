# -*- coding: utf-8 -*-

import pytest
import tuxbuild


@pytest.fixture(autouse=True)
def reset_config():
    tuxbuild.__config__ = None


@pytest.fixture
def params():
    return {
        "git_repo": "https://github.com/torvalds/linux.git",
        "git_ref": "master",
        "target_arch": "arm64",
        "toolchain": "gcc-9",
        "kconfig": ["defconfig"],
    }


def test_new_build(config, params):
    build = tuxbuild.Build(**params)
    assert build.token is not None
    assert build.kbapi_url is not None


def test_validate_auth_token_only_once(config, params, mocker):
    check_auth_token = mocker.patch("tuxbuild.config.Config.check_auth_token")
    tuxbuild.Build(**params)
    tuxbuild.Build(**params)
    assert check_auth_token.call_count == 1


def test_new_build_invalid_token(config, params, mocker):
    check_auth_token = mocker.patch("tuxbuild.config.Config.check_auth_token")
    check_auth_token.side_effect = RuntimeError("INVALID TOKEN")
    with pytest.raises(tuxbuild.exceptions.InvalidToken):
        tuxbuild.Build(**params)


def test_new_build_set(config, params):
    build_set = tuxbuild.BuildSet([params])
    assert build_set.kbapi_url is not None
