# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Functions for interacting with the OpenMW VFS
"""

import os
from logging import error, warning
from typing import Dict, List, Set
from .repo.list import read_list
from .globals import env
from .util import ci_exists
from .repo.loader import load_all_installed
from .tsort import tsort, CycleException
from .repo.config import read_userconfig, usedep_matches_installed
from .repo.usestr import check_required_use, use_reduce
from .repo.atom import Atom, atom_sat


def sort_vfs_if_needed(user_function):
    """
    Decorator that sorts the vfs before executing the given function
    if it is necessary
    """

    def decorating_function(*args, **kwargs):
        if vfs_needs_sorting():
            try:
                sort_vfs()
                clear_vfs_sort()
            except CycleException as err:
                error("{}", err)
        return user_function(*args, **kwargs)

    return decorating_function


@sort_vfs_if_needed
def find_file(name: str) -> str:
    """
    Locates the path of a file within the OpenMW virtual file system
    """
    for directory in get_vfs_dirs():
        path = ci_exists(os.path.join(directory, name))
        if path:
            return path

    raise FileNotFoundError(name)


@sort_vfs_if_needed
def list_dir(name: str) -> List[str]:
    """
    Locates all path of files matching the given pattern within the OpenMW
    virtual file system
    """
    files: Dict[str, str] = {}

    for directory in get_vfs_dirs():
        path = ci_exists(os.path.join(directory, name))
        if path:
            for file in os.listdir(path):
                if file.lower() not in files:
                    files[file.lower()] = os.path.join(path, file)

    return sorted(files.values())


def get_vfs_dirs() -> List[str]:
    """Returns an ordered list of the VFS directories, in reverse order of priority"""
    return read_list(os.path.join(env.MOD_DIR, "vfs"))


def __set_vfs_dirs__(dirs: List[str]):
    """Updates the vfs directories"""
    with open(os.path.join(env.MOD_DIR, "vfs"), "w") as vfs_file:
        for directory in dirs:
            print(directory, file=vfs_file)


def require_vfs_sort():
    """
    Creates a file that indicates the vfs still needs to be sorted
    """
    open(os.path.join(env.PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete"), "a").close()


def clear_vfs_sort():
    """Clears the file indicating the config needs sorting"""
    path = os.path.join(env.PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete")
    if os.path.exists(path):
        os.remove(path)


def vfs_needs_sorting():
    """Returns true if changes have been made since the config was sorted"""
    return os.path.exists(
        os.path.join(env.PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete")
    )


def sort_vfs():
    """Regenerates the vfs list"""
    print("Sorting VFS order...")

    installed_dict = load_all_installed()
    installed = [mod for group in installed_dict.values() for mod in group]

    graph = {}
    priorities = {}

    # Keys refer to master atoms (overridden).
    # values are a set of overriding mod atomso
    user_config_path = os.path.join(env.PORTMOD_CONFIG_DIR, "config", "install.csv")
    userconfig: Dict[str, Set[str]] = read_userconfig(user_config_path)

    # Determine all Directories that are enabled
    for mod in installed:
        for install in mod.INSTALL_DIRS:
            if check_required_use(
                install.REQUIRED_USE, mod.INSTALLED_USE, mod.valid_use
            ):
                default = os.path.normpath(install.PATCHDIR) == "."
                path = mod.get_dir_path(install)
                graph[(mod.CM, path, default)] = set()
                priorities[(mod.CM, path, default)] = mod.TIER

    # Validate entries in userconfig
    for entry in userconfig.keys() | {
        item for group in userconfig.values() for item in group
    }:
        possible_mods = installed_dict.get(Atom(entry).MN, [])
        if not possible_mods:
            warning(f"Mod {entry} in {user_config_path} is not installed!")
        elif len(possible_mods) > 1:
            warning(
                f"Mod {entry} in {user_config_path} is ambiguous! "
                f"It could refer to any of {mod.CMR for mod in possible_mods}"
            )

    # Add edges in the graph for each data override
    for mod in installed:
        for install in mod.INSTALL_DIRS:
            if check_required_use(
                install.REQUIRED_USE, mod.INSTALLED_USE, mod.valid_use
            ):
                idefault = os.path.normpath(install.PATCHDIR) == "."
                ipath = mod.get_dir_path(install)
                parents = set(
                    use_reduce(
                        mod.DATA_OVERRIDES + " " + install.DATA_OVERRIDES,
                        mod.INSTALLED_USE,
                        flat=True,
                        token_class=Atom,
                    )
                ) | {
                    Atom(override)
                    for name in userconfig
                    for override in userconfig[name]
                    if atom_sat(mod.ATOM, Atom(name))
                }

                for parent in parents:
                    if not usedep_matches_installed(parent):
                        continue

                    for (atom, path, default) in graph:
                        if atom_sat(Atom(atom), parent) and default:
                            if Atom(atom).BLOCK:
                                # Blockers have reversed edges
                                graph[(mod.CM, ipath, idefault)].add(
                                    (atom, path, default)
                                )
                            else:
                                graph[(atom, path, default)].add(
                                    (mod.CM, ipath, idefault)
                                )
    try:
        sorted_mods = tsort(graph, priorities)
    except CycleException as error:
        raise CycleException(
            "Encountered cycle when sorting vfs!", error.cycle
        ) from error

    new_dirs = [path for _, path, _ in sorted_mods]
    __set_vfs_dirs__(new_dirs)
