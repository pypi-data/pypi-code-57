# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Functions to set up and tear down a testing environment
"""

import os
import shutil
import git
from typing import Any, Dict, List
from portmod.globals import env
from portmod.config import get_config
from portmod.repos import Repo
from portmod.util import onerror
from portmod.main import sync
import portmod.repo.loader as loader

TEST_REPO_DIR = os.path.join(os.path.dirname(__file__), "testrepo")
TEST_REPO = Repo("test", TEST_REPO_DIR, False, None, None, -1000)
_TMP_FUNC = None
TESTDIR: str
OLD: Dict[str, Any]
OLD_CWD: str
OLD_REPOS: List[Repo]


def set_test_repo():
    """Replaces the repo list with one that just contains the test repo"""
    global OLD_REPOS

    OLD_REPOS = env.REPOS
    env.REPOS = [TEST_REPO]


def setup_env(profile):
    """
    Sets up an entire testing environment
    All file writes will occur within a temporary directory as a result
    """
    global OLD, OLD_CWD, TESTDIR

    cwd = os.getcwd()
    get_config.cache_clear()
    OLD = env.__dict__
    OLD_CWD = cwd
    TESTDIR = os.path.join(env.TMP_DIR, "test")
    env.PORTMOD_LOCAL_DIR = os.path.join(TESTDIR, "local")
    env.MOD_DIR = os.path.join(TESTDIR, "local", "mods")
    env.INSTALLED_DB = os.path.join(TESTDIR, "local", "db")
    env.PORTMOD_CONFIG_DIR = os.path.join(TESTDIR, "config")
    env.PORTMOD_CONFIG = os.path.join(TESTDIR, "config", "portmod.conf")
    env.CACHE_DIR = os.path.join(TESTDIR, "cache")
    env.PYBUILD_CACHE_DIR = os.path.join(TESTDIR, "cache", "pybuild")
    env.CONFIG_PROTECT_DIR = os.path.join(TESTDIR, "cache", "cfg_protect")
    env.REPOS_FILE = os.path.join(TESTDIR, "config", "repos.cfg")
    env.INTERACTIVE = False
    env.TESTING = True
    os.makedirs(env.PORTMOD_CONFIG_DIR, exist_ok=True)
    gitrepo = git.Repo.init(env.INSTALLED_DB)
    gitrepo.config_writer().set_value("commit", "gpgsign", False).release()
    gitrepo.config_writer().set_value("user", "email", "pytest@example.com").release()
    gitrepo.config_writer().set_value("user", "name", "pytest").release()
    os.makedirs(TESTDIR, exist_ok=True)
    os.makedirs(os.path.join(TESTDIR, "local"), exist_ok=True)
    set_test_repo()
    sync()
    select_profile(profile)
    return {
        "testdir": TESTDIR,
        "config": f"{TESTDIR}/config.cfg",
        "config_ini": f"{TESTDIR}/config.ini",
    }


def tear_down_env():
    """
    Reverts env to original state
    """
    os.chdir(OLD_CWD)
    env.__dict__ = OLD
    get_config.cache_clear()
    loader.cache.clear()
    shutil.rmtree(TESTDIR, onerror=onerror)


def unset_profile():
    """Removes the profile link"""
    linkpath = os.path.join(TESTDIR, "config", "profile")
    if os.path.exists(linkpath):
        os.unlink(linkpath)


def select_profile(profile):
    """Selects the given test repo profile"""
    linkpath = os.path.join(TESTDIR, "config", "profile")
    unset_profile()
    os.symlink(os.path.join(TEST_REPO_DIR, "profiles", profile), linkpath)
