# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

# File for interacting with PORTMOD_CONFIG/repos.cfg

import sys
import os
import ast
import logging
from types import SimpleNamespace
from portmod.globals import env
import configparser


class Repo(SimpleNamespace):
    def __init__(self, name, location, auto_sync, sync_type, sync_uri, priority):
        self.name = name
        self.location = location
        self.auto_sync = auto_sync
        self.sync_type = sync_type
        self.sync_uri = sync_uri
        self.priority = priority


# Parses list of repos from repos.cfg
def get_repos():
    repo_config = configparser.ConfigParser()
    repos = []
    default_repo = Repo(
        "openmw",
        os.path.join(env.PORTMOD_LOCAL_DIR, "openmw"),
        True,
        "git",
        env.REPO,
        -1000,
    )
    if not os.path.exists(env.REPOS_FILE):
        repos.append(default_repo)
    else:
        repo_config.read(env.REPOS_FILE)

        if "openmw" not in repo_config:
            repos.append(default_repo)

        for name, conf in repo_config.items():
            if name == "DEFAULT":
                # Ignore DEFAULT key, as it is always there. We will not use it
                continue

            # Repo must at least have a location
            if "location" in conf:
                repos.append(
                    Repo(
                        name,
                        os.path.expanduser(conf.get("location")),
                        ast.literal_eval(conf.get("auto_sync", "False")),
                        conf.get("sync_type"),
                        conf.get("sync_uri"),
                        int(conf.get("priority", 0)),
                    )
                )
            else:
                logging.warning(
                    'Repo "{}" is missing a location. Skipping...'.format(name)
                )

    # Sort repos by priority such that the highest priority appears first
    repos.sort(key=lambda x: x.priority, reverse=True)
    # Append the path for each repo to sys.path so that the pyclass dir can
    # be loaded as a module
    for repo in repos:
        sys.path.append(os.path.join(repo.location))

    return repos


def has_repo(name: str) -> bool:
    """Returns true iff the repo exists"""
    for repo in env.REPOS:
        if repo.name == name:
            return True
    return False


def get_repo(name: str) -> Repo:
    """Returns repo of the given name"""
    for repo in env.REPOS:
        if repo.name == name:
            return repo
    raise Exception(f"Cannot find repo of name {name}")
