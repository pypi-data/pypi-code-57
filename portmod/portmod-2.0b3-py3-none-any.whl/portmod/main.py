# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Iterable, Optional, Set, Tuple

import sys
import os
import argparse
import io
import traceback
import git
import shutil
import logging
from logging import error, info, warning
from pkg_resources import parse_version
from colorama import Fore
from portmod.repos import Repo
from portmod.globals import env, get_version
from portmod.repo.atom import Atom, atom_sat, InvalidAtom
from portmod.repo.loader import (
    load_mod,
    full_load_file,
    load_installed_mod,
    load_all_installed,
)
from portmod.transactions import (
    generate_transactions,
    print_transactions,
    sort_transactions,
    Trans,
    Transactions,
    UseDep,
)
from portmod.repo.deps import resolve, ModDoesNotExist, AmbigiousAtom, DepError
from portmod.repo.util import select_mod, KeywordDep, LicenseDep
from portmod.repo.sets import add_set, get_set, remove_set
from portmod.repo.keywords import add_keyword
from portmod.colour import lblue, colour, green, lgreen, red, bright
from portmod.mod import install_mod, remove_mod
from portmod.prompt import prompt_bool
from portmod.repo.metadata import get_repo_root
from portmod.query import query, display_search_results
from portmod.repo.download import is_downloaded, fetchable, get_download
from portmod.repo.manifest import create_manifest
from portmod.news import update_news, display_unread_message
from .vfs import (
    sort_vfs,
    require_vfs_sort,
    clear_vfs_sort,
    vfs_needs_sorting,
)
from .tsort import CycleException
from .repo.use import add_use
from .repo.usestr import check_required_use
from .repo.profiles import get_system
from .config import config_to_string, get_config
from .pybuild import FullPybuild
from .repos import has_repo
from .log import init_logger, add_logging_arguments
from .modules import require_module_updates, update_modules, clear_module_updates


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Command line interface to manage OpenMW mods"
    )
    parser.add_argument("mods", metavar="MOD", help="Mods to install", nargs="*")
    parser.add_argument(
        "--sync", help="Fetches and updates repository", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--depclean",
        help="Removes mods and their dependencies. \
        Will also remove mods dependent on the given mods",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--auto-depclean",
        help="Automatically removed unneeded dependencies "
        "after any other operation performed",
        action="store_true",
    )
    parser.add_argument(
        "-C",
        "--unmerge",
        help="Removes the given mods without checking dependencies.",
        action="store_true",
    )
    parser.add_argument(
        "--no-confirm",
        help="Doesn't ask for confirmation when installing or removing mods",
        action="store_true",
    )
    parser.add_argument(
        "-1",
        "--oneshot",
        help="Do not make any changes to the world set when \
        installing or removing mods",
        action="store_true",
    )
    parser.add_argument(
        "-O",
        "--nodeps",
        help="Ignore dependencies when installing specified mods. Note: This may cause mods \
        to fail to install if their build dependencies aren't satisfied, and fail to \
        work if their runtime dependencies aren't satisfied",
        action="store_true",
    )
    add_logging_arguments(parser)
    parser.add_argument(
        "-n",
        "--noreplace",
        help="Skips packages specified on the command line that have already been "
        "installed. Implied by options such as newuse and update",
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--update",
        help="Updates mods to the best version available and excludes packages \
        if they are already up to date.",
        action="store_true",
    )
    parser.add_argument(
        "-N",
        "--newuse",
        help="Includes mods whose use flags have changed since they were last \
        installed",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--emptytree",
        help="Reinstalls target atoms and their entire deep dependency tree, as \
        if no mods are currently installed",
        action="store_true",
    )
    parser.add_argument(
        "-D",
        "--deep",
        help="Consider entire dependency tree when doing dependency resolution \
        instead of just the immediate dependencies [unimplemented]",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Searches the repository for mods with the given phrase in their name",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--searchdesc",
        help="Searches the repository for mods with the given phrase in their name \
        or description",
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--select",
        type=str2bool,
        nargs="?",
        const=True,
        default=None,
        help="Adds specified mods to the world set",
    )
    parser.add_argument(
        "--deselect",
        type=str2bool,
        nargs="?",
        const=True,
        default=None,
        help="Removes specified mods from the world set. This is implied by uninstall \
        actions such as --depclean and --unmerge. Use --deselect=n to prevent \
        uninstalls from removing mods from the world set",
    )
    # TODO: Ensure that installed mods database matches mods that are actually installed
    parser.add_argument(
        "--validate",
        help="Checks if the mods in the mod directory are installed, and that the \
        directories in the config all exist",
        action="store_true",
    )
    parser.add_argument(
        "--sort-vfs",
        help="Sorts the vfs list. This is for debugging purposes, as the vfs is \
        normally sorted as necessary.",
        action="store_true",
    )
    parser.add_argument("--debug", help="Enables debug traces", action="store_true")
    parser.add_argument(
        "--ignore-default-opts",
        help="Causes the OMWMERGE_DEFAULT_OPTS environment variable to be ignored",
        action="store_true",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--version", help="Displays the version number of Portmod", action="store_true"
    )
    group.add_argument(
        "--info",
        help="Displays the values of several global variables for debugging purposes",
        action="store_true",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Ensure that we read config entries into os.environ
    get_config()

    if "--ignore-default-opts" in sys.argv:
        args = sys.argv[1:]
    else:
        args = sys.argv[1:] + os.environ.get("OMWMERGE_DEFAULT_OPTS", "").split()
    return parser.parse_args(args)


def sync():
    for repo in env.REPOS:
        if repo.auto_sync and repo.sync_type == "git":

            if os.path.exists(repo.location):
                info("Syncing repo {}...", repo.name)
                gitrepo = git.Repo.init(repo.location)
                current = gitrepo.head.commit

                # Remote location has changed. Update gitrepo to match
                if gitrepo.remotes.origin.url != repo.sync_uri:
                    gitrepo.remotes.origin.set_url(repo.sync_uri)

                gitrepo.remotes.origin.fetch()
                gitrepo.head.reset("origin/master", True, True)

                for diff in current.diff("HEAD"):
                    if diff.renamed_file:
                        print(
                            "{} {} -> {}".format(
                                diff.change_type, diff.a_path, diff.b_path
                            )
                        )
                    if diff.deleted_file:
                        print("{} {}".format(diff.change_type, diff.a_path))
                        if diff.a_path.endswith(".pybuild"):
                            # Remove from pybuild cache
                            parts = diff.a_path.split("/")
                            category = parts[0]
                            file = parts[-1].lstrip(".pybuild")
                            path = os.path.join(
                                env.PYBUILD_CACHE_DIR, repo.name, category, file
                            )
                            if os.path.exists(path):
                                os.remove(path)
                    else:
                        print("{} {}".format(diff.change_type, diff.b_path))

                tags = []
                for tag in gitrepo.tags:
                    # Valid tags must have the tag commit be the merge base
                    # A merge base further back indicates a branch point
                    if tag.name.startswith("portmod_v"):
                        base = gitrepo.merge_base(gitrepo.head.commit, tag.commit)
                        if base and base[0] == tag.commit:
                            tags.append(tag)

                this_version = get_version()
                newest = max(
                    [parse_version(tag.name.lstrip("portmod_v")) for tag in tags]
                    + [parse_version(this_version)]
                )
                if newest != parse_version(this_version) and not env.TESTING:
                    warning(
                        "A new version of Portmod is available. It is highly "
                        "recommended that you update as soon as possible, as "
                        "we do not provide support for outdated versions"
                    )
                    warning(f"Current Version: {this_version}")
                    warning(f"New Version:     {newest}")
                info("Done syncing repo {}", repo.name)
            else:
                git.Repo.clone_from(repo.sync_uri, repo.location)
                print("Initialized Repository")
        elif repo.auto_sync:
            error(
                'Sync type "{}" for repo "{}" is not supported. '
                "Supported types are: git",
                repo.sync_type,
                repo.name,
            )

    if os.path.exists(env.PYBUILD_CACHE_DIR):
        for repo in os.listdir(env.PYBUILD_CACHE_DIR):
            path = os.path.join(env.PYBUILD_CACHE_DIR, repo)
            if repo != "installed" and not has_repo(repo):
                print(
                    f'Cleaning up cache for repository "{repo}" which no longer exists'
                )
                shutil.rmtree(path)

    update_news()


def configure_mods(
    atoms: Iterable[str],
    *,
    delete: bool = False,
    depclean: bool = False,
    auto_depclean: bool = False,
    no_confirm: bool = False,
    oneshot: bool = False,
    verbose: bool = False,
    update: bool = False,
    newuse: bool = False,
    noreplace: bool = False,
    nodeps: bool = False,
    deselect: Optional[bool] = None,
    select: Optional[bool] = None,
    deep: bool = False,
    emptytree: bool = False,
):
    # Ensure that we always get the config before performing operations on mods
    # This way the config settings will be available as environment variables.
    get_config()

    targetlist = list(atoms)
    for modstr in targetlist:
        if modstr.startswith("@"):
            # Atom is actually a set. Load set instead
            targetlist.extend(get_set(modstr.replace("@", "")))
            continue

    to_remove = set()
    if delete or depclean:
        for modstr in targetlist:
            if modstr.startswith("@"):
                continue

            skip = False
            atom = Atom(modstr)
            for system_atom in get_system():
                if atom_sat(atom, system_atom):
                    warning("Skipping removal of system mod {}", modstr)
                    skip = True
                    break

            if not skip:
                to_remove.add(atom)

    atomlist = [
        Atom(modstr)
        for modstr in targetlist
        if modstr not in to_remove and not modstr.startswith("@")
    ]

    if delete:
        # Do nothing. We don't care about deps
        transactions = Transactions()
        for atom in to_remove:
            mod = load_installed_mod(atom)
            if not mod:
                raise Exception(f"Mod {modstr} is not installed!")
            transactions.append(Trans.DELETE, mod)
    elif nodeps:
        fqatoms = []
        for atom in atomlist:
            mod, _ = select_mod(load_mod(atom))
            fqatoms.append(mod.ATOM)

        newselected: Set[Atom]
        if oneshot:
            newselected = set()
        else:
            newselected = {Atom(atom.CMN) for atom in fqatoms}

        transactions = generate_transactions(
            fqatoms, [], newselected, [], noreplace=noreplace, emptytree=emptytree,
        )
    else:
        transactions = resolve(
            atomlist,
            to_remove,
            deep=deep
            or (depclean and not to_remove),  # No argument depclean implies deep
            update=update,
            newuse=newuse,
            noreplace=noreplace or depclean or update or newuse,
            depclean=auto_depclean or depclean,
            emptytree=emptytree,
        )

    transactions = sort_transactions(transactions)

    # Inform user of changes
    if transactions.mods:
        # Don't print transaction list when in quiet mode and no-confirm is passed
        if not no_confirm or logging.root.level < logging.WARN:
            if delete or depclean:
                print("These are the mods to be removed, in order:")
            else:
                print("These are the mods to be installed, in order:")
            print_transactions(transactions, verbose=verbose)
            print()
    elif vfs_needs_sorting() and not transactions.mods:
        global_updates()
        info("Nothing else to do.")
        return
    elif not transactions.mods:
        info("Nothing to do.")
        return

    if transactions.config:
        keyword_changes = list(
            filter(lambda x: isinstance(x, KeywordDep), transactions.config)
        )
        license_changes = list(
            filter(lambda x: isinstance(x, LicenseDep), transactions.config)
        )
        use_changes = list(filter(lambda x: isinstance(x, UseDep), transactions.config))
        if keyword_changes:
            print(
                "The following keyword changes are necessary to proceed.\n"
                "This will enable enable the installation of a mod that is unstable "
                '(if keyword is prefixed by a "~"), or untested, (if keyword is "**")'
            )
            for keyword in keyword_changes:
                if keyword.keyword.startswith("*"):
                    c = Fore.RED
                else:
                    c = Fore.YELLOW
                print(
                    "    {} {}".format(green(keyword.atom), colour(c, keyword.keyword))
                )

            if no_confirm or prompt_bool(
                "Would you like to automatically apply these changes?"
            ):
                for keyword in keyword_changes:
                    add_keyword(keyword.atom, keyword.keyword)
            else:
                return

        if license_changes:
            # TODO: For EULA licenses, display the license and prompt the user to accept
            print(
                "The following licence changes are necessary to proceed. "
                "Please review these licenses and make the changes manually."
            )
            for license in license_changes:
                print("    {} {}".format(green(license.atom), license.license))
            return

        if use_changes:
            print("The following use flag changes are necessary to proceed. ")
            for use in use_changes:
                if use.flag.startswith("-") and use.oldvalue == use.flag.lstrip("-"):
                    print(
                        "    {} {} # Note: currently enabled!".format(
                            lblue(use.atom), red(use.flag)
                        )
                    )
                elif not use.flag.startswith("-") and use.oldvalue == "-" + use.flag:
                    print(
                        "    {} {} # Note: currently disabled!".format(
                            green(use.atom), red(use.flag)
                        )
                    )
                else:
                    print("    {} {}".format(green(use.atom), red(use.flag)))
            if no_confirm or prompt_bool(
                "Would you like to automatically apply these changes?"
            ):
                for use in use_changes:
                    add_use(use.flag.lstrip("-"), use.atom, use.flag.startswith("-"))
            else:
                return

    def print_restricted_fetch(transactions: Transactions):
        # Check for restricted fetch mods and print their nofetch notices
        for (trans, mod) in transactions.mods:
            if trans != Trans.DELETE:
                can_fetch = fetchable(mod)
                to_fetch = [
                    source
                    for source in mod.get_default_sources()
                    if get_download(source.name, source.hashes) is None
                ]
                if set(to_fetch) - set(can_fetch) and not is_downloaded(mod):
                    print(green("Fetch instructions for {}:".format(mod.ATOM)))
                    mod.UNFETCHED = to_fetch
                    mod.A = mod.get_default_sources()
                    mod.USE = mod.get_use()[0]
                    mod.mod_nofetch()
                    del mod.UNFETCHED
                    print()

    print_restricted_fetch(transactions)

    for (trans, mod) in transactions.mods:
        if trans != Trans.DELETE:
            # TODO: There are various variables that should be set on mod during mod_pretend
            mod.mod_pretend()

    if not (no_confirm or prompt_bool("Would you like to continue?")):
        return

    err = None
    merged = Transactions()
    messages = []
    # Install (or remove) mods in order
    for trans, mod in transactions.mods:
        if trans == Trans.DELETE:
            remove_mod(mod)
            if deselect is None or deselect:
                if mod.CMN in get_set("world"):
                    info(f"Removing {green(mod.CMN)} from world favourites file")
                    remove_set("world", mod.CMN)
            merged.mods.append((trans, mod))
        elif install_mod(mod):
            if mod in transactions.new_selected and not oneshot:
                if mod.CMN not in get_set("world"):
                    info(f"Adding {green(mod.CMN)} to world favourites file")
                    add_set("world", mod.CMN)
            merged.mods.append((trans, mod))
        else:
            # Unable to install mod. Aborting installing remaining mods
            err = mod.ATOM
            break

        mod_msg = []
        for msg in mod._warnings:
            mod_msg.append(("WARN", msg))
        for msg in mod._info:
            mod_msg.append(("INFO", msg))

        if mod_msg:
            messages.append((mod.ATOM.CMF, mod_msg))
        require_vfs_sort()
        require_module_updates()

    for pkg, msgs in messages:
        print()
        print(f">>> Messages for package {bright(green(pkg))}:")
        for typ, msg in msgs:
            if typ == "WARN":
                warning(msg)
            elif typ == "INFO":
                info(msg)
        print()

    # Commit changes to installed database
    gitrepo = git.Repo.init(env.INSTALLED_DB)
    try:
        gitrepo.head.commit
    except ValueError:
        gitrepo.git.commit(m="Initial Commit")

    transstring = io.StringIO()
    print_transactions(merged, verbose=True, out=transstring, summarize=False)
    if gitrepo.git.diff("HEAD", cached=True):
        # There was an error. We report the mods that were successfully merged and
        # note that an error occurred, however we still commit anyway.
        if err:
            gitrepo.git.commit(
                m=(
                    "Successfully merged {} mods. Error occurred when attempting to "
                    "merge {}\n{}".format(
                        len(transactions.mods), err, transstring.getvalue()
                    )
                )
            )
        else:
            gitrepo.git.commit(
                m="Successfully merged {} mods: \n{}".format(
                    len(transactions.mods), transstring.getvalue()
                )
            )

    # Check if mods need to be added to rebuild set
    if plugin_changed(merged.mods):
        for mod in query("REBUILD", "ANY_PLUGIN", installed=True):
            if mod.ATOM not in [mod.ATOM for (trans, mod) in merged.mods]:
                add_set("rebuild", mod.CMN)

    # Check if mods were just rebuilt and can be removed from the rebuild set
    for installed_mod in query("REBUILD", "ANY_PLUGIN", installed=True):
        if installed_mod.ATOM in [mod.ATOM for (trans, mod) in merged.mods]:
            remove_set("rebuild", installed_mod.CMN)

    # Check if mods in the rebuild set were just removed
    for (trans, mod) in transactions.mods:
        if "ANY_PLUGIN" in mod.REBUILD:
            remove_set("rebuild", mod.CMN)

    if get_set("rebuild"):
        warning("The following mods need to be rebuilt:")
        for atom in get_set("rebuild"):
            print("    {}".format(green(atom)))
        print("Use {} to rebuild these mods".format(lgreen("omwmerge @rebuild")))

    global_updates()


def plugin_changed(mods: Iterable[Tuple[Trans, FullPybuild]]):
    for (_, mod) in mods:
        for idir in mod.INSTALL_DIRS:
            for plug in getattr(idir, "PLUGINS", []):
                if check_required_use(
                    plug.REQUIRED_USE, mod.get_use()[0], mod.valid_use
                ) and check_required_use(
                    idir.REQUIRED_USE, mod.get_use()[0], mod.valid_use
                ):
                    return True


def global_updates():
    """Performs updates to global configuration"""
    # Update module set.
    for mod in get_set("modules", parent_dir=env.PORTMOD_LOCAL_DIR):
        if not load_installed_mod(Atom(mod)):
            # Note: safe because this doesn't modify the set returned by get_set
            remove_set("modules", mod, parent_dir=env.PORTMOD_LOCAL_DIR)

    for mod in load_all_installed(flat=True):
        if "module" in mod.PROPERTIES:
            add_set("modules", mod.CMN, parent_dir=env.PORTMOD_LOCAL_DIR)

    # Fix vfs ordering and update modules
    try:
        sort_vfs()
        clear_vfs_sort()
        update_modules()
        clear_module_updates()
    except CycleException as e:
        error("{}", e)


def deselect(mods: Iterable[str], *, no_confirm: bool = False):
    all_to_remove = []

    for name in mods:
        atom = Atom(name)
        to_remove = None
        for mod in get_set("selected"):
            if atom_sat(mod, atom):
                if to_remove:
                    raise Exception(
                        f"Atom {name} is ambiguous and could match either "
                        f"{to_remove} or {mod}! "
                        "Please re-run using a fully qualified Atom."
                    )
                to_remove = mod

        if to_remove:
            info(f'>>> Removing {green(to_remove)} from "world" favourites file')
            all_to_remove.append(to_remove)

    if not all_to_remove:
        print('>>> No matching atoms found in "world" favourites file...')
        return

    if no_confirm or prompt_bool(
        bright("Would you like to remove these mods from your world favourites?")
    ):
        for mod in all_to_remove:
            remove_set("world", mod)


def filter_mods(mods):
    from portmod.repo.loader import load_all
    from portmod.repo.util import get_hash
    from shutil import move

    atoms = []
    os.makedirs(env.DOWNLOAD_DIR, exist_ok=True)

    for mod in mods:
        if os.path.isfile(mod):
            for atom in load_all():
                for source in atom.get_sources(matchall=True):
                    if get_hash(mod) == source.hashes[0].value:
                        move(mod, os.path.join(env.DOWNLOAD_DIR, mod))
                        atoms.append(atom.ATOM)
        else:
            atoms.append(mod)

    return atoms


def main():
    os.environ["PYTHONUNBUFFERED"] = "1"

    args = parse_args()
    atoms = filter_mods(args.mods)

    env.DEBUG = args.debug

    init_logger(args)

    if args.version:
        print(f"Portmod {get_version()}")

    if args.info:
        # Print config values
        config = get_config()
        if args.verbose:
            print(config_to_string(config))
        else:
            print(
                config_to_string(
                    {
                        entry: config[entry]
                        for entry in config
                        if entry in config["INFO_VARS"]
                    }
                )
            )
        # Print hardcoded portmod paths
        print(f"TMP_DIR = {env.TMP_DIR}")
        print(f"CACHE_DIR = {env.CACHE_DIR}")
        print(f"PORTMOD_CONFIG_DIR = {env.PORTMOD_CONFIG_DIR}")
        print(f"PORTMOD_LOCAL_DIR = {env.PORTMOD_LOCAL_DIR}")

    if args.validate:
        # Check that mods in the DB correspond to mods in the mods directory
        for category in os.listdir(env.INSTALLED_DB):
            if not category.startswith("."):
                for mod in os.listdir(os.path.join(env.INSTALLED_DB, category)):
                    # Check that mod is installed
                    if not os.path.exists(
                        os.path.join(env.INSTALLED_DB, category, mod)
                    ):
                        error(
                            f"Mod {category}/{mod} is in the portmod database, but "
                            "is not installed!"
                        )

                    # Check that pybuild can be loaded
                    if not load_installed_mod(Atom(f"{category}/{mod}")):
                        error(f"Installed mod {category}/{mod} could not be loaded")

        # Check that all mods in the mod directory are also in the DB
        for category in os.listdir(env.MOD_DIR):
            for mod in os.listdir(os.path.join(env.MOD_DIR, category)):
                if not os.path.exists(os.path.join(env.INSTALLED_DB, category, mod)):
                    error(
                        f"Mod {category}/{mod} is installed but "
                        "is not in the portmod database!"
                    )

    if args.sync:
        sync()

    if args.search:
        mods = query(
            ["NAME", "ATOM"],
            " ".join(atoms),
            strip=True,
            squelch_sep=True,
            insensitive=True,
        )
        display_search_results(mods)
        return

    if args.searchdesc:
        mods = query(
            ["NAME", "ATOM", "DESC"],
            " ".join(atoms),
            strip=True,
            squelch_sep=True,
            insensitive=True,
        )

        display_search_results(mods)
        return

    if args.nodeps and args.depclean:
        error(
            "--nodeps and --depclean cannot be used together. "
            "If you want to remove mods without checking dependencies, please use "
            "--unmerge"
        )
        sys.exit(1)

    if atoms or args.depclean:
        # If deselect is supplied (is not None), only deselect if not removing.
        # If removing, remove normally, but deselect depending on supplied value.
        if args.deselect and not (args.unmerge or args.depclean):
            deselect(atoms, no_confirm=args.no_confirm)
        else:
            try:
                configure_mods(
                    atoms,
                    delete=args.unmerge,
                    depclean=args.depclean,
                    no_confirm=args.no_confirm,
                    oneshot=args.oneshot,
                    verbose=args.verbose,
                    update=args.update,
                    newuse=args.newuse,
                    noreplace=args.noreplace or args.update or args.newuse,
                    nodeps=args.nodeps,
                    deselect=args.deselect,
                    select=args.select,
                    auto_depclean=args.auto_depclean,
                    deep=args.deep,
                    emptytree=args.emptytree,
                )
            except (InvalidAtom, ModDoesNotExist, AmbigiousAtom, DepError) as e:
                if args.debug:
                    traceback.print_exc()
                error("{}", e)
            except Exception as e:
                # Always print stack trace for Unknown exceptions
                traceback.print_exc()
                error("{}", e)

    if args.sort_vfs:
        global_updates()

    display_unread_message()


def pybuild_validate(file_name):
    # Verify that pybuild is valid python
    import py_compile

    py_compile.compile(file_name, doraise=True)

    # Verify fields of pybuild
    mod = full_load_file(file_name)
    mod.validate()


def pybuild_manifest(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError("Pybuild file {} does not exist".format(file_name))

    repo_root = get_repo_root(file_name)

    if repo_root is None:
        raise FileNotFoundError("Cannot find repository for the given file. ")

    # Register repo in case it's not already in repos.cfg
    REAL_ROOT = os.path.realpath(repo_root)
    if not any([REAL_ROOT == os.path.realpath(repo.location) for repo in env.REPOS]):
        sys.path.append(os.path.join(repo_root))
        env.REPOS.append(
            Repo(os.path.basename(repo_root), repo_root, False, None, None, 0)
        )

    if env.ALLOW_LOAD_ERROR:
        raise Exception("Cannot allow load errors when generating manifest!")

    mod = full_load_file(file_name)

    create_manifest(mod)
    info(f"Created Manifest for {mod.ATOM}")
