# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests profile loading
"""

import pytest
from pathlib import Path
from .env import setup_env, tear_down_env, unset_profile
from portmod.repo.profiles import get_profile_path, profile_parents, get_system
from portmod.repo.loader import load_all_installed
from portmod.main import configure_mods


@pytest.fixture(autouse=False)
def setup_repo():
    """sets up and tears down test environment"""
    yield setup_env("test")
    tear_down_env()


def test_profile_parents(setup_repo):
    """Tests that all profile parents are resolved correctly"""
    for parent in profile_parents():
        assert Path(parent).resolve()


def test_profile_nonexistant(setup_repo):
    """
    Tests that portmod behaves as expected when the profile does not exist
    """
    unset_profile()
    with pytest.raises(Exception):
        get_profile_path()


def test_system(setup_repo):
    """
    Tests that the system set behaves as expected
    """
    system = get_system()
    assert "test/test" in system

    assert not load_all_installed(flat=True)
    configure_mods(["@world"], update=True, no_confirm=True)
    mods = load_all_installed(flat=True)
    assert len(mods) == len(system)
    for mod in mods:
        assert mod.CMN in system
    for name in system:
        assert any(mod.CMN == name for mod in mods)
