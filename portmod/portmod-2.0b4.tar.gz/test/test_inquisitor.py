# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Portmod config tests
"""

import pytest
from logging import error
from portmod.inquisitor import scan
from .env import setup_env, tear_down_env, TEST_REPO


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_inquisitor():
    """
    Basic inquisitor test on test repo
    """
    has_error = False

    def err(string: str):
        nonlocal has_error
        error(string)
        has_error = True

    scan(TEST_REPO.location, err)
    if has_error:
        raise Exception("Inqusitor failed. See error log for details.")


# TODO: Add tests that modify the test repo to be invalid
