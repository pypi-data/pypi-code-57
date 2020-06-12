# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Config sorting tests
"""

import os
import pytest
from portmod.globals import env
from portmod.main import configure_mods
from portmod.tsort import CycleException
from portmod.repo.use import add_use
from portmod.vfs import get_vfs_dirs, sort_vfs
from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test-config")
    config = dictionary["config"]
    config_ini = dictionary["config_ini"]
    with open(env.PORTMOD_CONFIG, "w") as configfile:
        print(
            f"""
TEST_CONFIG = "{config}"
TEST_CONFIG_INI = "{config_ini}"
""",
            file=configfile,
        )
    yield dictionary
    tear_down_env()


def test_sort_vfs(setup):
    """
    Tests that sorting the config files works properly
    """
    # Install mods
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    testdir = setup["testdir"]

    path1 = os.path.join(testdir, "local", "mods", "test", "test")
    path2 = os.path.join(testdir, "local", "mods", "test", "test2")

    # Check that config is correct
    lines = get_vfs_dirs()
    assert path1 in lines
    assert path2 in lines
    assert lines.index(path1) < lines.index(path2)

    # Remove mods
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True, depclean=True)

    # Check that config is no longer contains their entries
    assert not get_vfs_dirs()


def test_user_override(setup):
    """
    Tests that user overrides for vfs sorting work properly
    """

    testdir = setup["testdir"]
    installpath = os.path.join(testdir, "config", "config", "install.csv")
    os.makedirs(os.path.dirname(installpath), exist_ok=True)

    path1 = os.path.join(testdir, "local", "mods", "test", "test")
    path2 = os.path.join(testdir, "local", "mods", "test", "test2")

    # Enforce that test overrides test2
    with open(installpath, "w") as file:
        print("test/test, test/test2", file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)

    # Check that config is correct
    lines = get_vfs_dirs()
    assert path1 in lines
    assert path2 in lines
    assert lines.index(path1) > lines.index(path2)

    # Enforce that test2 overrides test
    with open(installpath, "w") as file:
        print("test/test2, test/test", file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)

    # Check that config is correct
    lines = get_vfs_dirs()
    assert path1 in lines
    assert path2 in lines
    assert lines.index(path1) < lines.index(path2)

    os.remove(installpath)
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True, depclean=True)


def test_user_cycle(setup):
    """
    Tests that cycles introduced by the user are reported correctly
    """
    testdir = setup["testdir"]
    installpath = os.path.join(testdir, "config", "config", "install.csv")
    os.makedirs(os.path.dirname(installpath), exist_ok=True)

    # Enforce that test overrides test2
    with open(installpath, "w") as file:
        print("test/test, test/test2", file=file)
        print("test/test2, test/test", file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    with pytest.raises(CycleException):
        sort_vfs()

    os.remove(installpath)
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True, depclean=True)


def test_data_override_flag(setup):
    """
    Tests that mods can conditionally override other mods using DATA_OVERRIDES
    depending on the value of a use flag on the target mod
    """
    # Install mods
    configure_mods(["test/test6-1.0", "test/test7-1.0"], no_confirm=True)
    testdir = setup["testdir"]

    path1 = os.path.join(testdir, "local", "mods", "test", "test6")
    path2 = os.path.join(testdir, "local", "mods", "test", "test7")

    # Check that config is correct
    lines = get_vfs_dirs()
    assert path1 in lines
    assert path2 in lines
    assert lines.index(path1) < lines.index(path2)

    add_use("foo")
    configure_mods(["test/test7-1.0"], no_confirm=True)

    lines = get_vfs_dirs()
    assert path1 in lines
    assert path2 in lines
    assert lines.index(path1) > lines.index(path2)

    # Remove mods
    configure_mods(["test/test6-1.0", "test/test7-1.0"], no_confirm=True, depclean=True)

    # Check that config is no longer contains their entries
    assert not get_vfs_dirs()
