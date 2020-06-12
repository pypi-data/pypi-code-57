# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Depclean tests
"""

import pytest
from portmod.main import configure_mods, deselect
from portmod.repo.loader import load_installed_mod, load_all_installed
from portmod.repo import Atom
from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_depclean(setup):
    """
    Tests that deselected mods are then depcleaned
    """
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    mod = load_installed_mod(Atom("test/test2"))
    assert mod in load_all_installed(flat=True)
    deselect(["test/test2"], no_confirm=True)
    configure_mods([], no_confirm=True, depclean=True)
    assert mod not in load_all_installed(flat=True)

    mod = load_installed_mod(Atom("test/test"))
    assert mod in load_all_installed(flat=True)
    deselect(["test/test"], no_confirm=True)
    configure_mods([], no_confirm=True, depclean=True)
    # Note: test/test is a system mod, so it cannot be removed
    assert mod in load_all_installed(flat=True)
