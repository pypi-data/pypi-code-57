# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re
import sys
from enum import Enum
from typing import AbstractSet, Any, Dict, Iterable, List, Optional, Set, Tuple, cast

from .colour import blue, bright, green, lgreen, red, yellow
from .config import get_config
from .pybuild import FullPybuild, InstalledPybuild, Pybuild
from .query import get_flag_string
from .repo.atom import Atom, FQAtom, atom_sat, version_gt
from .repo.loader import load_installed_mod, load_mod, full_load_mod
from .repo.manifest import get_download_size
from .repo.sets import is_selected
from .repo.use import get_use
from .repo.usestr import use_reduce
from .repo.util import select_mod
from .repo.flags import collapse_flags
from .tsort import CycleException, tsort


class ModDoesNotExist(Exception):
    """Indicates that no mod matching this atom could be loaded"""


class Trans(Enum):
    DELETE = "d"
    NEW = "N"
    UPDATE = "U"
    DOWNGRADE = "D"
    REINSTALL = "R"


class Transactions:
    mods: List[Tuple[Trans, FullPybuild]]
    config: Set[Any]
    new_selected: Set[FullPybuild]

    def __init__(self):
        self.mods = []
        self.config = set()
        self.new_selected = set()

    def copy(self) -> "Transactions":
        new = Transactions()
        new.mods = self.mods.copy()
        new.config = self.config.copy()
        new.new_selected = self.new_selected.copy()
        return new

    def append(self, trans: Trans, mod: Pybuild):
        self.mods.append((trans, full_load_mod(mod)))

    def add_new_selected(self, mod: Pybuild):
        self.new_selected.add(full_load_mod(mod))

    def extend(self, trans: "Transactions"):
        self.mods.extend(trans.mods)
        self.config |= trans.config
        self.new_selected |= trans.new_selected

    def find(self, mod: Pybuild) -> Optional[Tuple[Trans, Pybuild]]:
        for trans, other in self.mods:
            if mod == other:
                return (trans, other)
        return None


class UseDep:
    def __init__(self, atom: Atom, flag: str, oldvalue: Optional[str]):
        self.atom = atom
        self.flag = flag
        self.oldvalue = oldvalue


def get_usestrings(
    mod: Pybuild,
    installed_use: Optional[Set[str]],
    verbose: bool,
    transactions: Transactions,
) -> List[str]:
    enabled_use, disabled_use = get_use(mod)
    for use in filter(lambda x: isinstance(x, UseDep), transactions.config):
        if atom_sat(mod.ATOM, use.atom):
            if use.flag.startswith("-"):
                enabled_use.remove(use.flag.lstrip("-"))
            else:
                enabled_use.add(use.flag)

    # Note: flags containing underscores are USE_EXPAND flags
    # and are displayed separately
    IUSE_STRIP = {flag.lstrip("+") for flag in mod.IUSE if "_" not in flag}

    texture_options = use_reduce(
        mod.TEXTURE_SIZES, enabled_use, disabled_use, flat=True, token_class=int
    )

    use_expand_strings = []
    for use in get_config().get("USE_EXPAND", []):
        if use in get_config().get("USE_EXPAND_HIDDEN", []):
            continue

        flags = {
            re.sub(f"^{use.lower()}_", "", flag)
            for flag in mod.IUSE_EFFECTIVE
            if flag.startswith(f"{use.lower()}_")
        }
        if flags:
            enabled_expand = {
                val for val in get_config().get(use, "").split() if val in flags
            }
            disabled_expand = flags - enabled_expand
            installed_expand: Optional[Set[str]]
            if installed_use is not None:
                installed_expand = {
                    re.sub(f"^{use.lower()}_", "", flag)
                    for flag in installed_use
                    if flag.startswith(use.lower() + "_")
                }
            else:
                installed_expand = None
            string = get_flag_string(
                use, enabled_expand, disabled_expand, installed_expand, verbose=verbose
            )
            use_expand_strings.append(string)

    if mod.TEXTURE_SIZES is not None and len(texture_options) >= 2:
        texture_size = next(
            (
                use.lstrip("texture_size_")
                for use in enabled_use
                if use.startswith("texture_size")
            ),
            None,
        )
        if texture_size is not None:
            texture_string = get_flag_string(
                "TEXTURE_SIZE",
                [texture_size],
                map(str, sorted(set(texture_options) - {int(texture_size)})),
            )
        else:
            texture_string = ""
    else:
        texture_string = ""

    usestring = get_flag_string(
        "USE",
        enabled_use & IUSE_STRIP,
        IUSE_STRIP - enabled_use,
        installed_use,
        verbose=verbose,
    )

    return [usestring] + use_expand_strings + [texture_string]


def print_transactions(
    transactions: Transactions,
    verbose: bool = False,
    out=sys.stdout,
    summarize: bool = True,
):
    mods = transactions.mods
    download_size = get_download_size(
        [mod for (trans, mod) in mods if trans != Trans.DELETE]
    )

    for (trans, mod) in mods:
        installed_mod = load_installed_mod(Atom(mod.CMN))
        if installed_mod is None:
            installed_use = None
        else:
            installed_use = installed_mod.INSTALLED_USE

        v = verbose or trans == Trans.NEW
        oldver = ""

        if trans != Trans.DELETE:
            usestrings = get_usestrings(mod, installed_use, v, transactions)
            usestring = " ".join(list(filter(None, usestrings)))
        else:
            usestring = ""

        if trans == Trans.DELETE:
            trans_colour = red
        elif trans == Trans.NEW:
            trans_colour = lgreen
        elif trans == Trans.REINSTALL:
            trans_colour = yellow
        elif trans in (Trans.DOWNGRADE, Trans.UPDATE):
            trans_colour = blue
            installed_mod = load_installed_mod(Atom(mod.CMN))
            oldver = blue(" [" + installed_mod.MVR + "]")

        modstring: str
        if verbose:
            modstring = mod.ATOM
        else:
            modstring = mod.ATOM.CMF

        if is_selected(mod.ATOM) or mod in transactions.new_selected:
            modstring = bright(green(modstring))
        else:
            modstring = green(modstring)

        print(
            "[{}] {}{}{}".format(
                bright(trans_colour(trans.value)), modstring, oldver, " " + usestring
            ),
            file=out,
        )

    if summarize:
        print(
            "Total: {} mods ({} updates, {} new, {} reinstalls, {} removals), "
            "Size of downloads: {}".format(
                len(mods),
                len(
                    [
                        trans
                        for (trans, _) in mods
                        if trans == Trans.UPDATE or trans == Trans.DOWNGRADE
                    ]
                ),
                len([trans for (trans, _) in mods if trans == Trans.NEW]),
                len([trans for (trans, _) in mods if trans == Trans.REINSTALL]),
                len([trans for (trans, _) in mods if trans == Trans.DELETE]),
                download_size,
            ),
            file=out,
        )


def get_all_deps(depstring: str) -> List[Atom]:
    dependencies = use_reduce(depstring, token_class=Atom, matchall=True, flat=True)

    # Note that any || operators will still be included. strip those out
    return list(
        [dep for dep in dependencies if dep != "||" and not dep.startswith("!")]
    )


def use_changed(installed: InstalledPybuild, flagupdates: Iterable[str] = []) -> bool:
    """
    Checks whether or not the use flag configuration for the given mod
    has changed since it was installed.
    """
    (enabled, _) = get_use(installed)
    enabled = set(filter(lambda x: x[0] != "-", collapse_flags(enabled, flagupdates)))
    return enabled != installed.INSTALLED_USE


def sort_transactions(transactions: Transactions):
    """
    Create graph and do a topological sort to ensure that mods are installed/removed
    in the correct order given their dependencies
    """

    def get_dep_graph(rdepend=True):
        graph: Dict[Atom, Set[Atom]] = {}
        priorities = {}

        for (trans, mod) in transactions.mods:
            graph[mod.ATOM] = set()
            priorities[mod.ATOM] = mod.TIER

        def add_depends(mod, key: str, delete: bool):
            depends = {}
            depstring = getattr(mod, key)
            for dep in get_all_deps(depstring):
                for (_, othermod) in transactions.mods:
                    if atom_sat(othermod.ATOM, dep):
                        depends[othermod.ATOM] = othermod

            if delete:
                # When removing mods, remove them before their dependencies
                graph[mod.ATOM] |= set(depends.keys())
            else:
                # When adding or updating mods, mods, add or update their dependencies
                # before them
                for dep in depends:
                    graph[dep].add(mod.ATOM)
                    if key == "DEPEND":
                        # Also ensure runtime dependencies are available for build dependencies
                        # Whether or not we enforce runtime dependencies for all mods
                        add_depends(depends[dep], "RDEPEND", False)

        for (trans, mod) in transactions.mods:
            add_depends(mod, "DEPEND", trans == Trans.DELETE)
            if rdepend:
                add_depends(mod, "RDEPEND", trans == Trans.DELETE)
        return graph, priorities

    # Attempt to sort using both runtime and build dependencies. If this fails,
    # fall back to just build dependencies
    graph, priorities = get_dep_graph()
    try:
        mergeorder = tsort(graph, priorities)
    except CycleException:
        try:
            graph, priorities = get_dep_graph(rdepend=False)
            mergeorder = tsort(graph, priorities)
        except CycleException:
            raise Exception(
                "Could not sort transactions; there is a cycle in dependency graph!"
            )

    new_trans = transactions.copy()
    new_trans.mods = []
    for atom in mergeorder:
        for (trans, mod) in transactions.mods:
            if mod.ATOM == atom:
                new_trans.mods.append((trans, mod))
                break

    return new_trans


def generate_transactions(
    enabled: Iterable[FQAtom],
    disabled: Iterable[FQAtom],
    newselected: AbstractSet[Atom],
    usedeps: Iterable[UseDep],
    *,
    noreplace: bool = False,
    emptytree: bool = False,
) -> Transactions:
    """
    Generates a list of transactions to update the system such that
    all mods in enabled are installed and all mods in disabled are not

    Mods will not be rebuilt unless a change has occurred, or they are included
    in the new_selected parameter set and noreplace is not specified.

    @param enabled: Mods that should be enabled, if not already
    @param disabled: Mods that should be disabled, if not already
    @param new_selected: Mods that were selected by the user for this operation
                         These should be re-installed, even if no change has been
                         made, unless noreplace is also passed
    @param usedeps: Use changes that should accompany the transactions
    @param noreplace: If true, don't re-install selected mods that haven't changed
    """
    transactions = Transactions()
    flagupdates: Dict[str, List[str]] = {}
    for dep in usedeps:
        if dep.atom in flagupdates:
            flagupdates[dep.atom].append(dep.flag)
        else:
            flagupdates[dep.atom] = [dep.flag]

    for atom in enabled:
        modlist = load_mod(atom)

        to_install: Optional[Pybuild]
        if modlist:
            assert len(modlist) == 1
            (to_install, dep) = select_mod(modlist)
        else:
            to_install = None
            dep = None
        installed = load_installed_mod(Atom(atom.CMN))

        if not (to_install or installed):
            raise ModDoesNotExist("Unable to find mod for atom {}".format(atom))

        if (
            to_install is not None
            and to_install.ATOM.CMN in newselected
            or (installed and installed.ATOM.CMN in newselected)
        ):
            transactions.add_new_selected(to_install or installed)

        if dep is not None:
            transactions.config.add(dep)

        if emptytree:
            transactions.append(Trans.REINSTALL, to_install or installed)
            continue

        # TODO: There might be advantages to preferring installed over to_install
        # such as avoiding re-downloading files just because the sources changed in a trivial
        # manner
        if installed is not None:
            installed.USE = get_use(installed)[0]
            if version_gt((to_install or installed).ATOM.MVR, installed.ATOM.MVR) or (
                "live"
                in use_reduce(installed.PROPERTIES, installed.INSTALLED_USE, flat=True)
                and full_load_mod(installed).can_update_live()
            ):
                transactions.append(Trans.UPDATE, to_install or installed)
            elif version_gt(installed.ATOM.MVR, (to_install or installed).ATOM.MVR):
                transactions.append(Trans.DOWNGRADE, to_install)
            elif use_changed(installed, flagupdates.get(installed.CM, [])):
                transactions.append(Trans.REINSTALL, to_install or installed)
            elif not noreplace and installed.ATOM.CMN in newselected:
                transactions.append(Trans.REINSTALL, to_install or installed)
        elif to_install is not None:
            new_mod = cast(Pybuild, to_install)
            transactions.append(Trans.NEW, new_mod)

    for atom in disabled:
        to_remove = load_installed_mod(Atom(atom))
        if to_remove is not None:
            transactions.append(Trans.DELETE, to_remove)

    # Only add usedeps that differ from their current setting
    # for the mod to be installed
    for dep in usedeps:
        for _, mod in transactions.mods:
            if atom_sat(mod.ATOM, dep.atom):
                enabled_use, _ = get_use(mod)
                if (
                    dep.flag[0] == "-"
                    and dep.flag.lstrip("-") in enabled_use
                    or dep.flag[0] != "-"
                    and dep.flag not in enabled_use
                ):
                    transactions.config.add(dep)

    return transactions
