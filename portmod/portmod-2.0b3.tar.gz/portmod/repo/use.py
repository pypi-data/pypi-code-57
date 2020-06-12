# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Set, Tuple

import os
import warnings
import logging
from functools import lru_cache
from portmod.globals import env
from portmod.repo.usestr import use_reduce
from portmod.repo.flags import get_flags, add_flag, remove_flag, collapse_flags
from portmod.repo.textures import select_texture_size
from ..config import get_config, read_config
from ..pybuild import Pybuild
from .profiles import profile_parents
from .atom import Atom


class InvalidFlag(Exception):
    """Exception indicating an invalid use flag"""


@lru_cache(maxsize=None)
def get_use_expand_flags() -> Set[str]:
    """Returns all currently enabled USE_EXPAND flags"""
    flags = set()
    for use in get_config().get("USE_EXPAND", []):
        if not use.startswith("-"):
            for flag in get_config().get(use, "").split():
                flags.add(f"{use.lower()}_{flag}")
    return flags


def get_user_global_use() -> Set[str]:
    """Returns user-specified global use flags"""
    return read_config(env.PORTMOD_CONFIG, {}).get("USE", set())


def get_user_use(atom: Atom) -> Set[str]:
    """Returns user-specified use flags for a given mod"""
    use_file = os.path.join(env.PORTMOD_CONFIG_DIR, "mod.use")
    if os.path.exists(use_file):
        return get_flags(use_file, atom)

    return set()


def get_forced_use(atom: Atom) -> Set[str]:
    """Returns a list of forced use flags for the given mod"""
    force: Set[str] = set()
    for parent_dir in profile_parents():
        force_file = os.path.join(parent_dir, "use.force")
        if os.path.exists(force_file):
            flags = get_flags(force_file)
            force = collapse_flags(force, flags)

        mod_force_file = os.path.join(parent_dir, "mod.use.force")
        if os.path.exists(mod_force_file):
            flags = get_flags(mod_force_file, atom)
            force = collapse_flags(force, flags)

    return force


def get_use(mod: Pybuild) -> Tuple[Set[str], Set[str]]:
    """Returns a list of enabled and a list of disabled use flags"""
    GLOBAL_USE = get_config().get("USE", [])
    use: Set[str] = set()
    for parent_dir in profile_parents():
        use_file = os.path.join(parent_dir, "mod.use")
        if os.path.exists(use_file):
            flags = get_flags(use_file, mod.ATOM)
            use = collapse_flags(use, flags)

    use = collapse_flags(use, GLOBAL_USE)

    # User config is the last added, overriding profile flags
    use = collapse_flags(use, get_user_use(mod.ATOM))

    # Forced use flags must be collapsed last to ensure that the
    # forced flags override any other values
    use = collapse_flags(use, get_forced_use(mod.ATOM))

    enabled_use = {x for x in use if not x.startswith("-")}
    disabled_use = {x.lstrip("-") for x in use if x.startswith("-")}

    enabled_use |= get_use_expand_flags()

    enabled_use = enabled_use.intersection(mod.IUSE_EFFECTIVE) | {
        x.lstrip("+")
        for x in mod.IUSE
        if x.startswith("+") and x.lstrip("+") not in disabled_use
    }

    disabled_use = disabled_use.intersection(mod.IUSE_EFFECTIVE)

    texture_sizes = use_reduce(
        mod.TEXTURE_SIZES, enabled_use, disabled_use, token_class=int
    )
    texture_size = select_texture_size(texture_sizes)
    if texture_size is not None:
        found = None
        for useflag in enabled_use:
            if useflag.startswith("texture_size_"):
                if not found:
                    found = useflag
                elif useflag != found:
                    raise Exception(
                        "Invalid use configuration. "
                        f"Multiple texture size options {use} and {found} "
                        f"enabled for mod {mod.ATOM}"
                    )
        enabled_use.add("texture_size_{}".format(texture_size))

    return (enabled_use, disabled_use)


def verify_use(flag, atom=None):
    from .loader import load_mod
    from .metadata import get_global_use

    if atom:
        return any(flag in mod.IUSE_EFFECTIVE for mod in load_mod(atom))
    else:
        return flag in [
            flag for repo in env.REPOS for flag in get_global_use(repo.location)
        ]


def add_use(flag, atom=None, disable=False):
    from portmod.repo import loader

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        from redbaron import RedBaron
        from redbaron.nodes import AssignmentNode, NameNode

    if disable and flag in get_config().get("USE", []):
        remove_use(flag, atom)

    disableflag = "-" + flag

    if (disable and flag in get_config().get("USE", [])) or (
        not disable and disableflag in get_config().get("USE", [])
    ):
        remove_use(flag, atom)

    if not verify_use(flag, atom):
        if atom:
            raise InvalidFlag(
                "{} is not a valid use flag for mod {}".format(flag, atom)
            )
        else:
            raise InvalidFlag("{} is not a valid global use flag".format(flag))
        return

    if atom is not None:
        from portmod.repo.util import select_mod

        (newest, req) = select_mod(loader.load_mod(atom))
        if flag not in newest.IUSE_EFFECTIVE:
            logging.warn(
                "{} is not a valid use flag for {}, "
                "the default selected version of mod {}".format(flag, newest.ATOM, atom)
            )

    if atom:
        use_file = os.path.join(env.PORTMOD_CONFIG_DIR, "mod.use")
        if disable:
            remove_flag(use_file, atom, flag)
            add_flag(use_file, atom, disableflag)
        else:
            remove_flag(use_file, atom, disableflag)
            add_flag(use_file, atom, flag)
    else:
        with open(env.PORTMOD_CONFIG, "r") as file:
            node = RedBaron(file.read())

        GLOBAL_USE = get_config()["USE"]
        get_config.cache_clear()

        if (not disable and flag not in GLOBAL_USE) or (
            disable and disableflag not in GLOBAL_USE
        ):
            if disable:
                print("Adding -{} to USE in portmod.conf".format(flag))
                GLOBAL_USE.add(disableflag)
            else:
                print("Adding {} to USE in portmod.conf".format(flag))
                GLOBAL_USE.add(flag)

            USE_STR = '"' + " ".join(sorted(GLOBAL_USE)) + '"'

            found = False
            for elem in node:
                if (
                    isinstance(elem, AssignmentNode)
                    and isinstance(elem.target, NameNode)
                    and elem.target.value == "USE"
                ):
                    elem.value = USE_STR
                    found = True

            if not found:
                node.append(f"USE = {USE_STR}")

            with open(env.PORTMOD_CONFIG, "w") as file:
                file.write(node.dumps())
        else:
            if disable:
                logging.warn(f'Use flag "{flag}" is already disabled globally')
            else:
                logging.warn(f'Use flag "{flag}" is already enabled globally')


def remove_use(flag, atom=None):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        from redbaron import RedBaron
        from redbaron.nodes import AssignmentNode, NameNode

    disableflag = "-" + flag

    if not verify_use(flag, atom):
        print("Warning: {} is not a valid use flag for mod {}".format(flag, atom))

    if atom is not None:
        use_file = os.path.join(env.PORTMOD_CONFIG_DIR, "mod.use")
        remove_flag(use_file, atom, flag)
        remove_flag(use_file, atom, disableflag)
    else:
        with open(env.PORTMOD_CONFIG, "r") as file:
            node = RedBaron(file.read())

        GLOBAL_USE = get_config()["USE"]
        get_config.cache_clear()

        if flag in GLOBAL_USE or disableflag in GLOBAL_USE:
            if flag in GLOBAL_USE:
                print("Removing {} from USE in portmod.conf".format(flag))
                GLOBAL_USE.remove(flag)

            if disableflag in GLOBAL_USE:
                print("Removing -{} from USE in portmod.conf".format(flag))
                GLOBAL_USE.remove(disableflag)

            USE_STR = '"' + " ".join(sorted(GLOBAL_USE)) + '"'

            for elem in node:
                if (
                    isinstance(elem, AssignmentNode)
                    and isinstance(elem.target, NameNode)
                    and elem.target.value == "USE"
                ):
                    elem.value = USE_STR

            with open(env.PORTMOD_CONFIG, "w") as file:
                file.write(node.dumps())
        else:
            logging.warn(f'Use flag "{flag}" is not set globally')


def satisfies_uselist(uselist, enabled):
    if len(uselist) == 0:
        return True

    for flag in uselist:
        if flag.startswith("-") and flag.lstrip("-") in enabled:
            return False
        elif not flag.startswith("-") and flag not in enabled:
            return False

    return True


# Determines if the uselist is satisfied for the mod in the current configuration
def satisfies_use(uselist, mod):
    return satisfies_uselist(uselist, mod.USE)
