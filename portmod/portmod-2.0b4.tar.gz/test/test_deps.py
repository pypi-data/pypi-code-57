# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Dependency resolution integration tests
"""

import pytest
from portmod.main import configure_mods
from portmod.repo.loader import load_installed_mod, load_all_installed
from portmod.repo import Atom
from portmod.repo.deps import DepError
from portmod.repo.use import get_use
from .env import setup_env, tear_down_env


@pytest.fixture(autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("base")  # Like test, but has no system mods
    yield dictionary
    tear_down_env()


def test_deps(setup):
    """
    Tests that dependencies resolve correctly
    """
    # test3 test4 and test5 should resolve correctly if
    # the foo flag is disabled for mod 3
    configure_mods(["test/test3", "test/test5"], no_confirm=True)
    mod3 = load_installed_mod(Atom("test/test3"))
    mod4 = load_installed_mod(Atom("test/test4"))
    mod5 = load_installed_mod(Atom("test/test5"))
    assert mod3 in load_all_installed(flat=True)
    assert mod4 in load_all_installed(flat=True)
    assert mod5 in load_all_installed(flat=True)
    assert "foo" not in get_use(mod3)[0]

    # test3, test4, test5, and test6 should not resolve correctly
    with pytest.raises(DepError):
        configure_mods(["test/test3", "test/test5", "test/test6"], no_confirm=True)


def test_unsolveable(setup):
    """Tests that mods that cannot be resolved fail to resolve"""

    with pytest.raises(DepError):
        configure_mods(["test/test-useless"], no_confirm=True)


def test_weight(setup):
    """Tests that mods which are not selected are not pulled in by the dependency calculation"""

    # Note test7 will cause other mods to be pulled into the formula due to conditionals,
    # but by default shouldn't depend on anything
    configure_mods(["test/test7"], no_confirm=True)
    assert len(load_all_installed(flat=True)) == 1
    assert all(mod.MN != "test" for mod in load_all_installed(flat=True))


def test_usedep_cli(setup):
    """Tests that use dependencies are satisfied when passed on the command line"""
    configure_mods(["test/test4[foo,bar,-baz]"], no_confirm=True)
    mod = load_installed_mod(Atom("test/test4"))
    assert mod
    assert mod.INSTALLED_USE >= {"foo", "bar"}
    assert "baz" not in mod.INSTALLED_USE
