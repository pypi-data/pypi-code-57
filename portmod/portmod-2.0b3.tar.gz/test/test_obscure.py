# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from collections.abc import Mapping

import pytest

from portmod.repo.loader import __load_file

from .env import setup_env, tear_down_env
from .test_loader import TMP_FILE, cleanup_tmp, create_pybuild


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_import_side_effects():
    """
    Tests for side effects when importing whitelisted python modules

    This specific instance is obscure, and it's not clear why it occurs, however
    avoiding using our custom import code for whitelisted modules avoids this causing
    an exception. See #135.
    """
    file = """
from pybuild import Pybuild1
import typing

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    create_pybuild(file)
    __load_file(TMP_FILE)
    cleanup_tmp()

    isinstance([], Mapping)
