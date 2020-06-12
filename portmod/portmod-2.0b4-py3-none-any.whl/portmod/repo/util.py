# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Various utility functions
"""

from typing import Any, Iterable, Tuple, Optional
import hashlib
from collections import namedtuple
from functools import lru_cache
from portmod.repo.keywords import accepts, accepts_testing, get_keywords
from portmod.repo.metadata import has_eula, is_license_accepted
from ..config import get_config
from ..pybuild import Pybuild
from .atom import version_gt

BUF_SIZE = 65536

KeywordDep = namedtuple("KeywordDep", ["atom", "keyword"])
LicenseDep = namedtuple("LicenseDep", ["atom", "license", "is_eula"])


def get_keyword_dep(mod: Pybuild) -> Optional[KeywordDep]:
    if not accepts(get_keywords(mod.ATOM), mod.KEYWORDS):
        arch = get_config()["ARCH"]
        if accepts_testing(arch, mod.KEYWORDS):
            return KeywordDep(mod.ATOM.CM, "~" + arch)
        return KeywordDep("=" + mod.ATOM.CM, "**")
    return None


def select_mod(modlist: Iterable[Pybuild]) -> Tuple[Pybuild, Any]:
    """
    Chooses a mod version based on keywords and accepts it if the license is accepted
    """
    if not modlist:
        raise Exception("Cannot select mod from empty modlist")

    filtered = list(
        filter(lambda mod: accepts(get_keywords(mod.ATOM), mod.KEYWORDS), modlist)
    )

    keyword = None

    if filtered:
        mod = get_newest_mod(filtered)
    else:
        arch = get_config()["ARCH"]
        # No mods were accepted. Choose the best version and add the keyword
        # as a requirement for it to be installed
        unstable = list(
            filter(lambda mod: accepts_testing(arch, mod.KEYWORDS), modlist)
        )
        if unstable:
            mod = get_newest_mod(unstable)
            keyword = "~" + arch
        else:
            # There was no mod that would be accepted by enabling testing.
            # Try enabling unstable
            mod = get_newest_mod(modlist)
            keyword = "**"

    if not is_license_accepted(mod):
        return (mod, LicenseDep(mod.CMN, mod.LICENSE, has_eula(mod)))
    if keyword is not None:
        return (mod, KeywordDep("=" + mod.ATOM.CMF, keyword))

    return (mod, None)


def get_max_version(versions: Iterable[str]) -> Optional[str]:
    """
    Returns the largest version in the given list

    Version should be a valid version according to PMS section 3.2,
    optionally follwed by a revision

    Returns None if the version list is empty
    """
    newest = None
    for version in versions:
        if newest is None or version_gt(version, newest):
            newest = version
    return newest


def get_newest_mod(modlist: Iterable[Pybuild]) -> Pybuild:
    """
    Returns the newest mod in the given list based on version
    If there is a tie, returns the earlier mod in the list
    """
    max_ver = get_max_version([mod.MVR for mod in modlist])
    for mod in modlist:
        if mod.MVR == max_ver:
            return mod
    raise Exception(
        f"Internal Error: get_max_version returned incorrect result {max_ver}"
    )


@lru_cache(maxsize=None)
def get_hash(filename: str, funcs=(hashlib.sha512,)) -> str:
    """Hashes the given file"""
    hash_funcs = [func() for func in funcs]
    with open(filename, mode="rb") as archive:
        while True:
            data = archive.read(BUF_SIZE)
            if not data:
                break
            for hash_func in hash_funcs:
                hash_func.update(data)
    return [str(hash_func.hexdigest()) for hash_func in hash_funcs]
