# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for performing bulk queries on the mod database and repositories
"""

from typing import AbstractSet, Dict, Generator, Iterable, List, Optional, Tuple, Union
import argparse
import re
import sys
import traceback
import logging
from .globals import env
from .colour import green, lgreen, blue, bright, lblue, red, yellow
from .config import get_config
from .pybuild import Pybuild
from .repo.manifest import get_total_download_size
from .repo.loader import load_all, load_all_installed, load_installed_mod
from .repo.util import get_newest_mod
from .repo.atom import Atom, atom_sat
from .repo.use import use_reduce, get_use
from .repo.metadata import get_mod_metadata


def compose(*functions):
    """
    Composes the given single-argument functions
    """

    def inner(arg):
        for func in reversed(functions):
            arg = func(arg)
        return arg

    return inner


def str_strip(value: str) -> str:
    return re.sub("(( +- +)|(:))", "", value)


def str_squelch_sep(value: str) -> str:
    return re.sub(r"[-_\s]+", " ", value)


def query(
    fields: Union[str, Iterable],
    value: str,
    strip: bool = False,
    squelch_sep: bool = False,
    insensitive: bool = False,
    installed: bool = False,
) -> Generator[Pybuild, None, None]:
    """
    Finds mods that contain the given value in the given field
    """

    def func(val: str) -> str:
        result = val
        if insensitive:
            result = result.lower()
        if strip:
            result = str_strip(result)
        if squelch_sep:
            result = str_squelch_sep(result)
        return result

    search = func(value)

    if installed:
        mods = [mod for group in load_all_installed().values() for mod in group]
    else:
        mods = load_all()

    for mod in mods:
        if isinstance(fields, str):
            if hasattr(mod, fields) and search in func(getattr(mod, fields)):
                yield mod
        else:
            if any(
                hasattr(mod, field) and search in func(getattr(mod, field))
                for field in fields
            ):
                yield mod


def query_depends(atom: Atom, all_mods=False) -> List[Tuple[Atom, str]]:
    """
    Finds mods that depend on the given atom
    """
    if all_mods:
        mods = load_all()
    else:
        mods = [mod for group in load_all_installed().values() for mod in group]

    depends = []
    for mod in mods:
        if not all_mods:
            enabled, disabled = get_use(mod)
            atoms = use_reduce(
                mod.RDEPEND, enabled, disabled, token_class=Atom, flat=True
            )
        else:
            atoms = use_reduce(mod.RDEPEND, token_class=Atom, matchall=True, flat=True)

        for dep_atom in atoms:
            if dep_atom != "||" and atom_sat(dep_atom, atom):
                depends.append((mod.ATOM, dep_atom))
    return depends


def get_flag_string(
    name: Optional[str],
    enabled: Iterable[str],
    disabled: Iterable[str],
    installed: Optional[AbstractSet[str]] = None,
    *,
    verbose: bool = True,
    display_minuses=True,
):
    """
    Displays flag configuration

    Enabled flags are displayed as blue
    If the installed flag list is passed, flags that differ from the
    installed set will be green
    if name is None, the name prefix will be omitted and no quotes will
    surround the flags
    """

    def disable(string: str) -> str:
        if display_minuses:
            return "-" + string
        return string

    flags = []
    for flag in sorted(enabled):
        if installed is not None and flag not in installed:
            flags.append(bright(lgreen(flag)))
        elif verbose:
            flags.append(red(bright(flag)))

    for flag in sorted(disabled):
        if installed is not None and flag in installed:
            flags.append(bright(lgreen(disable(flag))))
        elif verbose:
            if display_minuses:
                flags.append(blue(disable(flag)))
            else:
                flags.append(lblue(disable(flag)))

    inner = " ".join(flags)

    if not flags:
        return None

    if name:
        return f'{name}="{inner}"'

    return inner


def display_search_results(
    mods: Iterable[Pybuild], summarize: bool = True, file=sys.stdout
):
    """
    Prettily formats a list of mods for use in search results
    """
    groupedmods: Dict[str, List[Pybuild]] = {}
    for mod in mods:
        if groupedmods.get(mod.CMN) is None:
            groupedmods[mod.CMN] = [mod]
        else:
            groupedmods[mod.CMN].append(mod)

    sortedgroups = sorted(groupedmods.values(), key=lambda group: group[0].NAME)

    for group in sortedgroups:
        sortedmods = sorted(group, key=lambda mod: mod.MV)
        newest = get_newest_mod(group)
        installed = load_installed_mod(Atom(newest.CMN))
        download = get_total_download_size([newest])

        if installed is not None:
            installed_str = blue(bright(installed.MV))

            flags = {flag.lstrip("+") for flag in installed.IUSE if "_" not in flag}
            usestr = get_flag_string(
                None, installed.INSTALLED_USE & flags, flags - installed.INSTALLED_USE
            )
            texture_options = {
                size
                for mod in group
                for size in use_reduce(
                    installed.TEXTURE_SIZES, matchall=True, flat=True
                )
            }
            texture = next(
                (
                    use.lstrip("texture_size_")
                    for use in installed.INSTALLED_USE
                    if use.startswith("texture_size_")
                ),
                None,
            )
            if isinstance(texture, str):
                texture_string = get_flag_string(
                    "TEXTURE_SIZE", [texture], texture_options - {texture}
                )
            else:
                texture_string = None
            use_expand_strings = []
            for use in get_config().get("USE_EXPAND", []):
                if use in get_config().get("USE_EXPAND_HIDDEN", []):
                    continue
                flags = {
                    re.sub(f"^{use.lower()}_", "", flag)
                    for flag in installed.IUSE_EFFECTIVE
                    if flag.startswith(f"{use.lower()}_")
                }
                if flags:
                    enabled_expand = {
                        val for val in get_config().get(use, "").split() if val in flags
                    }
                    string = get_flag_string(
                        use, enabled_expand, flags - enabled_expand, None
                    )
                    use_expand_strings.append(string)

            installed_str += (
                " {"
                + " ".join(
                    list(filter(None, [usestr, texture_string] + use_expand_strings))
                )
                + "}"
            )
        else:
            installed_str = "not installed"

        # List of version numbers, prefixed by either (~) or ** depending on
        # keyword for user's arch. Followed by use flags, including use expand
        version_str = ""
        versions = []
        ARCH = get_config()["ARCH"]
        for mod in sortedmods:
            if ARCH in mod.KEYWORDS:
                versions.append(green(mod.MV))
            elif "~" + ARCH in mod.KEYWORDS:
                versions.append(yellow("(~)" + mod.MV))
            else:
                versions.append(red("**" + mod.MV))
        version_str = " ".join(versions)
        flags = {
            flag.lstrip("+") for mod in group for flag in mod.IUSE if "_" not in flag
        }
        usestr = get_flag_string(None, [], flags, display_minuses=False)
        texture_options = {
            size
            for mod in group
            for size in use_reduce(mod.TEXTURE_SIZES, matchall=True, flat=True)
        }
        texture_string = get_flag_string(
            "TEXTURE_SIZE", [], texture_options, display_minuses=False
        )
        use_expand_strings = []
        for use in get_config().get("USE_EXPAND", []):
            if use in get_config().get("USE_EXPAND_HIDDEN", []):
                continue
            flags = {
                re.sub(f"^{use.lower()}_", "", flag)
                for flag in mod.IUSE_EFFECTIVE
                for mod in group
                if flag.startswith(f"{use.lower()}_")
            }
            if flags:
                string = get_flag_string(use, [], flags, None, display_minuses=False)
                use_expand_strings.append(string)

        version_str += (
            " {"
            + " ".join(
                list(filter(None, [usestr, texture_string] + use_expand_strings))
            )
            + "}"
        )

        # If there are multiple URLs, remove any formatting from the pybuild and
        # add padding
        homepage_str = "\n                 ".join(newest.HOMEPAGE.split())
        mod_metadata = get_mod_metadata(mod)

        print(
            "{}  {}".format(green("*"), bright(newest.CMN)),
            "       {} {}".format(green("Name:"), mod.NAME),
            "       {} {}".format(green("Available Versions: "), version_str),
            "       {} {}".format(green("Installed version:  "), installed_str),
            "       {} {}".format(green("Size of files:"), download),
            "       {} {}".format(green("Homepage:"), homepage_str),
            "       {} {}".format(green("Description:"), str_squelch_sep(newest.DESC)),
            "       {} {}".format(green("License:"), newest.LICENSE),
            sep="\n",
            file=file,
        )

        def list_maintainers_to_human_strings(maintainers):
            """ return the list of maintainers as a human readible string """
            result = ""
            for maintainer_id in range(len(maintainers)):
                maintainer = str(maintainers[maintainer_id])
                if maintainer_id >= len(maintainers) - 1:  # the last
                    result += maintainer
                elif maintainer_id >= len(maintainers) - 2:  # the second last
                    result += maintainer + " and "
                else:
                    result += maintainer + ", "
            return result

        if mod_metadata and mod_metadata.get("upstream"):
            maintainers = mod_metadata["upstream"].get("maintainer")
            if maintainers:
                if not isinstance(maintainers, list):
                    maintainers = [maintainers]

                maintainers_display_strings = list_maintainers_to_human_strings(
                    maintainers
                )
                print(
                    "       {} {}".format(
                        green("Upstream Author/Maintainer:"),
                        maintainers_display_strings,
                    ),
                    file=file,
                )

        print(file=file)

    if summarize:
        print("\nMods found: {}".format(len(sortedgroups)), file=file)


def query_main():
    """
    Main function for omwquery executable
    """
    parser = argparse.ArgumentParser(
        description="Command line interface to query information about portmod mods"
    )
    parser.add_argument("--debug", help="Enables debug traces", action="store_true")
    subparsers = parser.add_subparsers()
    depends = subparsers.add_parser(
        "depends", help="list all mods directly depending on ATOM"
    )
    depends.add_argument("ATOM")
    depends.add_argument(
        "-a",
        "--all",
        help="Also query mods that are not installed",
        action="store_true",
    )

    def depends_func(args):
        print(" * These mods depend on {}:".format(bright(args.ATOM)))
        for mod_atom, dep_atom in query_depends(Atom(args.ATOM), args.all):
            print("{} ({})".format(green(mod_atom), dep_atom))

    depends.set_defaults(func=depends_func)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.debug:
        env.DEBUG = True
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            traceback.print_exc()
            logging.error("{}".format(e))
            sys.exit(1)
