# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests modifying user use flags
"""

import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

import pytest
from portmod.globals import env
from portmod.main import main, sync
from portmod.repos import get_repos

from .env import setup_env, tear_down_env, unset_profile


@pytest.fixture(scope="module", autouse=True)
def setup():
    """sets up and tears down test environment"""
    dictionary = setup_env("test")
    env.REPOS = get_repos()
    # Unset profile so news is marked as old
    unset_profile()
    yield dictionary
    tear_down_env()


def test_logging():
    """Tests that verbose and quiet control output verbosity"""
    oldargs = sys.argv
    sync()
    sys.argv = ["", "--sync", "--quiet"]
    output = StringIO()
    with redirect_stdout(output):
        with redirect_stderr(output):
            main()

    assert not output.getvalue()

    sys.argv = ["", "--sync", "--verbose"]
    output = StringIO()
    with redirect_stdout(output):
        with redirect_stderr(output):
            main()

    assert output.getvalue()

    sys.argv = oldargs
