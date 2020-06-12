# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os

import pytest

from portmod.globals import env
from portmod.main import configure_mods
from portmod.modules import get_redirections

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_module(setup):
    """Tests that modules work as expected"""
    configure_mods(["test/test-module"], no_confirm=True)
    assert os.path.exists(os.path.join(env.CACHE_DIR, "cfg_protect", "foo.cfg_protect"))
    assert get_redirections()
