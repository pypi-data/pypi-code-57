# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Helper functions for interacting with repository metadata files.
"""

from typing import Dict, List, Optional, Set, Tuple, Union
import os
import glob
from functools import lru_cache
from portmod.yaml import yaml_load
from portmod.repo.list import read_list
from portmod.globals import env
from .usestr import use_reduce
from ..config import get_config
from ..config import read_config
from ..repos import get_repo, Repo
from ..pybuild import Pybuild
from .use import get_use


@lru_cache()
def __get_layout(repo_path) -> Dict:
    path = os.path.join(repo_path, "metadata", "layout.conf")
    if os.path.exists(path):
        return read_config(path, {})
    return {}


@lru_cache()
def get_masters(repo_path: str) -> List[Repo]:
    """Returns the direct masters for the repository at the given path"""
    masters = []
    for master in __get_layout(repo_path).get("masters", "").split():
        masters.append(get_repo(master))
    return masters


@lru_cache()
def get_repo_name(path: str) -> Optional[str]:
    """
    Given a path within a repo, returns the repo's name

    If path is not within a repo, returns None
    """
    root = get_repo_root(path)
    if root is None:
        return None
    path = os.path.join(root, "profiles", "repo_name")
    if os.path.exists(path):
        with open(path, mode="r") as name_file:
            return name_file.read().strip()
    return None


@lru_cache()
def get_repo_root(path: str) -> Optional[str]:
    """
    Returns the root given a path within a repository

    If the path is not in a repository, returns None
    """
    path = os.path.abspath(path)
    # Recursively look for metadata/repo_name to identify root
    if os.path.exists(os.path.join(path, "profiles", "repo_name")):
        return path
    if os.path.dirname(path) == path:
        # We've reached the root of the FS there is no repo
        return None

    return get_repo_root(os.path.dirname(path))


@lru_cache()
def get_categories(repo: str) -> Set[str]:
    """Retrieves the list of categories given a path to a repo"""
    categories: Set[str] = set()
    path = os.path.join(repo, "profiles", "categories")
    if os.path.exists(path):
        categories |= set(read_list(path))
    for master in get_masters(repo):
        categories |= get_categories(master.location)

    return categories


@lru_cache()
def get_archs(repo: str) -> Set[str]:
    """Returns the available architectures in a given repo"""
    archs: Set[str] = set()
    path = os.path.join(repo, "profiles", "arch.list")
    if os.path.exists(path):
        archs |= set(read_list(path))

    for master in get_masters(repo):
        archs |= get_archs(master.location)

    return set(read_list(path))


@lru_cache()
def get_global_use(repo) -> Dict[str, str]:
    """
    Returns the global use flag declarations for a given repository

    Each mapping in the result dictionary represents a use flag
    and its description
    """
    use: Dict[str, str] = {}
    path = os.path.join(repo, "profiles", "use.yaml")
    if os.path.exists(path):
        with open(path, mode="r") as use_file:
            use.update(yaml_load(use_file))

    for master in get_masters(repo):
        use.update(get_global_use(master.location))

    return use


@lru_cache()
def get_profiles() -> List[Tuple[str, str, str]]:
    """
    Returns the list of profiles available from all known repositories

    Result is a tuple containing the profile's path, name and stability keyword
    """
    profiles: List[Tuple[str, str, str]] = []
    for repo in env.REPOS:
        path = os.path.join(repo.location, "profiles", "profiles.yaml")
        if os.path.exists(path):
            with open(path, mode="r") as use_file:
                repo_profiles = yaml_load(use_file)
                for keyword in repo_profiles:
                    for profile in repo_profiles[keyword]:
                        path = os.path.join(repo.location, "profiles", profile)
                        profiles.append(
                            (path, profile, repo_profiles[keyword][profile])
                        )
    return profiles


@lru_cache()
def license_exists(repo: str, name: str) -> bool:
    """
    Returns true if the given license name corresponds to a
    licence in the repository
    """
    path = os.path.join(repo, "licenses", name)
    if os.path.exists(path):
        return True

    for master in get_masters(repo):
        if license_exists(master.location, name):
            return True

    return False


@lru_cache()
def has_eula(mod: Pybuild) -> bool:
    groups = get_license_groups(get_repo_root(mod.FILE))
    # FIXME: This should be reworked.
    # For one thing, this doesn't currently handle || operators
    return any(
        license_name in groups.get("EULA")
        for license_name in use_reduce(
            mod.LICENSE, get_use(mod)[0], get_use(mod)[1], flat=True
        )
    )


@lru_cache()
def get_license(repo: str, name: str) -> str:
    """Returns the full content of the named license"""
    path = os.path.join(repo, "licenses", name)
    if os.path.exists(path):
        with open(path, mode="r") as license_file:
            return license_file.read()
    else:
        for master in get_masters(repo):
            license_contents = get_license(master.location, name)
            if license is not None:
                return license_contents

        raise Exception("Nonexistant license: {}".format(name))


@lru_cache()
def get_license_groups(repo: str) -> Dict[str, Set[str]]:
    """
    Returns license groups defined by this repository and its masters

    @param repo: path to repository
    @returns set of license groups
    """
    result = {}
    path = os.path.join(repo, "profiles", "license_groups.yaml")
    if os.path.exists(path):
        with open(path, mode="r") as group_file:
            groups = yaml_load(group_file)

        for name, values in groups.items():
            if values is not None:
                result[name] = set(values.split())
            else:
                result[name] = set()

    def substitute(group: str):
        groups = []
        for license in result[group]:
            if license.startswith("@"):
                groups.append(license)
        for subgroup in groups:
            result[group].remove(subgroup)
            substitute(subgroup.lstrip("@"))
            result[group] |= result[subgroup.lstrip("@")]

    for group in result:
        substitute(group)

    for master in get_masters(repo):
        result.update(get_license_groups(master.location))

    return result


def is_license_accepted(mod: Pybuild) -> bool:
    """
    Returns true if the mod's license(s) are accepted by the user's configuration

    For a license to be accepted, it must be both listed, either explicitly,
    part of a group, or with the * wildcard  and it must not be blacklisted
    by a license or license group prefixed by a '-'
    """
    if mod.INSTALLED:
        license_groups = get_license_groups(get_repo(mod.REPO).location)
    else:
        license_groups = get_license_groups(get_repo_root(mod.FILE))

    ACCEPT_LICENSE = get_config()["ACCEPT_LICENSE"]

    def accepted(group: Union[str, List]) -> bool:
        if not group:
            return True

        if isinstance(group, str):
            allowed = False
            # Check if license is allowed by anything in ACCEPT_LICENSE
            for license in ACCEPT_LICENSE:
                if license.startswith("-") and (
                    license == group
                    or (license[1] == "@" and group in license_groups[license[2:]])
                ):
                    # not allowed if matched by this
                    return False
                if license == "*":
                    allowed = True
                if license.startswith("@") and group in license_groups[license[1:]]:
                    allowed = True
            return allowed
        elif group[0] == "||":
            return any(accepted(license) for license in group)
        else:
            return all(accepted(license) for license in group)

    enabled, disabled = get_use(mod)
    return accepted(use_reduce(mod.LICENSE, enabled, disabled, opconvert=True))

    # TODO: implement mod-specific license acceptance via mod.license config file


# TODO: Mod and category metadata structure should be explicitly defined.
@lru_cache()
def get_mod_metadata(mod: Pybuild):
    """Loads the metadata file for the given mod"""
    path = os.path.join(os.path.dirname(mod.FILE), "metadata.yaml")
    if not os.path.exists(path):
        return None

    with open(path, mode="r") as metadata_file:
        metadata = yaml_load(metadata_file)

    return metadata


@lru_cache()
def get_category_metadata(repo: str, category: str):
    """Loads the metadata file for the given category"""
    path = os.path.join(repo, category, "metadata.yaml")

    if os.path.exists(path):
        with open(path, mode="r") as metadata_file:
            metadata = yaml_load(metadata_file)
        return metadata

    for master in get_masters(repo):
        metadata = get_category_metadata(master.location, category)
        if metadata is not None:
            return metadata

    return None


@lru_cache()
def get_use_expand(repo: str) -> Set[str]:
    """Returns all possible use expand values for the given repository"""
    groups = set()
    for file in glob.glob(os.path.join(repo, "profiles", "desc", "*.yaml")):
        use_expand, _ = os.path.splitext(os.path.basename(file))
        groups.add(use_expand.upper())
    for master in get_masters(repo):
        groups |= get_use_expand(master.location)

    return groups


@lru_cache()
def check_use_expand_flag(repo: str, variable: str, flag: str) -> bool:
    """
    Returns true if the given use flag is declared
    in a USE_EXPAND desc file for the given variable
    """
    path = os.path.join(repo, "profiles", "desc", variable.lower() + ".yaml")
    if os.path.exists(path):
        with open(path, mode="r") as file:
            if flag in yaml_load(file):
                return True

    for master in get_masters(repo):
        if check_use_expand_flag(master.location, variable, flag):
            return True

    return False
