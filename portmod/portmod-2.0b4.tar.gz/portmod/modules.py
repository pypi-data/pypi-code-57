# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Interface for interacting with installed modules
"""

import csv
import glob
import os
import shutil
from collections import namedtuple
from difflib import unified_diff
from typing import Iterable, List
from logging import info

from .globals import env
from .mod import get_mod_path
from .prompt import prompt_options
from .repo.loader import __load_module_file, load_installed_mod
from .repo.sets import get_set
from .repo.list import read_list, add_list
from .pybuild import Pybuild
from .io_guard import Permissions

ModuleState = namedtuple("ModuleState", ["TEMP", "ROOT", "CACHE", "VERSION"])


def do_func(state, func, args=None):
    # Note: This must always be set prior to any module function execution
    # (which takes a state object), given that modules can modify the state object
    # and we set permissions based on the state object.
    # Fortunately we usually only run one function from a module at a time
    __PERMS = Permissions(  # noqa
        rw_paths=[state.TEMP, state.ROOT, state.CACHE, env.CONFIG_PROTECT_DIR],
        global_read=True,
    )
    if args is None:
        func(state)
    else:
        func(state, args)


class ModuleFunction:
    """Function defined by a module"""

    name: str

    def __init__(self, name: str, do, options, parameters, state: ModuleState):
        self.name = name
        self.__do__ = do
        self.state = state
        if options is not None:
            self.options = options()
        else:
            self.options = []
        if parameters is not None:
            self.parameters = parameters()
        else:
            self.parameters = []

    def do(self, args):
        """Execute action"""
        do_func(self.state, self.__do__, args)

    def do_update(self):
        """Execute update action"""
        do_func(self.state, self.__do__)

    def describe(self) -> str:
        """Returns string describing function"""
        return self.__do__.__doc__


class Module:
    """Base module object"""

    def __init__(self, name: str, desc: str, funcs: List[ModuleFunction], state):
        self.funcs = {func.name: func for func in funcs}
        self.name = name
        self.desc = desc
        self.state = state
        os.makedirs(state.TEMP, exist_ok=True)
        os.makedirs(state.CACHE, exist_ok=True)

    def update(self):
        if "update" in self.funcs:
            self.funcs["update"].do_update()

    def add_parser(self, parsers):
        parser = parsers.add_parser(self.name, help=self.desc)
        this_subparsers = parser.add_subparsers()
        for func in self.funcs.values():
            if func.name == "update":
                continue
            func_parser = this_subparsers.add_parser(func.name, help=func.describe())
            for option, parameter in zip(func.options, func.parameters):
                func_parser.add_argument(option, help=parameter)
            func_parser.set_defaults(func=func.do)

        def help_func(args):
            parser.print_help()

        parser.set_defaults(func=help_func)
        self.arg_parser = parser

        return self.arg_parser

    def cleanup(self):
        shutil.rmtree(self.state.TEMP)


def get_state(mod: Pybuild) -> ModuleState:
    return ModuleState(
        os.path.join(env.TMP_DIR, mod.CATEGORY, mod.MN, "temp"),
        os.path.join(env.MOD_DIR, mod.CATEGORY, mod.MN),
        os.path.join(env.CACHE_DIR, "pkg", mod.CATEGORY, mod.MN),
        mod.MV,
    )


def update_modules():
    """Runs update function (if present) on all installed modules"""
    for atom in get_set("modules", parent_dir=env.PORTMOD_LOCAL_DIR):
        mod = load_installed_mod(atom)
        for module_file in glob.glob(os.path.join(get_mod_path(mod), "*.pmodule")):
            module = __load_module_file(module_file, get_state(mod))
            module.update()
            module.cleanup()

    handle_cfg_protect()


def handle_cfg_protect():
    """Prompts user to allow changes to files made by modules"""
    whitelist_file = os.path.join(
        env.PORTMOD_LOCAL_DIR, "module-data", "file-whitelist"
    )
    blacklist_file = os.path.join(
        env.PORTMOD_LOCAL_DIR, "module-data", "file-blacklist"
    )
    blacklist = set()
    whitelist = set()
    if os.path.exists(whitelist_file):
        whitelist = set(read_list(whitelist_file))
    if os.path.exists(blacklist_file):
        blacklist = set(read_list(blacklist_file))

    # Display file changes to user and prompt
    for src, dst in get_redirections():
        src_data = None
        dst_data = None
        if os.path.islink(src):
            src_lines = ["symlink to " + os.readlink(src) + "\n"]
        else:
            try:
                with open(src, "r") as src_file:
                    src_lines = src_file.readlines()
            except UnicodeDecodeError:
                src_lines = ["<Binary data>\n"]
                with open(src, "rb") as src_file:
                    src_data = src_file.read()
        dst_lines = []
        if os.path.exists(dst):
            if os.path.islink(dst):
                dst_lines = ["symlink to " + os.readlink(dst) + "\n"]
            else:
                try:
                    with open(dst, "r") as dst_file:
                        dst_lines = dst_file.readlines()
                except UnicodeDecodeError:
                    dst_lines = ["<Binary data>\n"]
                    with open(dst, "rb") as dst_file:
                        dst_data = dst_file.read()

        if src_lines == dst_lines and src_data == dst_data:
            continue

        if dst in blacklist:
            info(f'Skipped change to blacklisted file "{dst}"')
            continue

        output = unified_diff(dst_lines, src_lines, dst, src)
        if dst in whitelist:
            # User won't be prompted, so we should still display output, but supress it
            # unless running verbosely
            info("".join(output))
        else:
            print("".join(output))

        print()

        if dst not in whitelist and not env.INTERACTIVE:
            info("Skipped update to file {} as mode is not interactive", dst)
            continue

        if dst not in whitelist:
            response = prompt_options(
                "Would you like to apply the above change?",
                [
                    ("y", "Apply change"),
                    (
                        "a",
                        "Apply change now, and whitelist this file so that you "
                        "aren't prompted again in future. Note that you will be"
                        " informed of changes to the file.",
                    ),
                    ("n", "Do not apply the change to this file"),
                    (
                        "N",
                        "never apply changes to this file. Note that you will "
                        "be informed when changes are attempted",
                    ),
                ],
            )

        if dst in whitelist or response in ("y", "a"):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)

        if response == "a":
            add_list(whitelist_file, dst)

        if response == "N":
            add_list(blacklist_file, dst)

    if env.INTERACTIVE:
        clear_redirections()


def add_parsers(parsers) -> List[Module]:
    """Adds parsers for the modules to the given argument parser"""
    modules = []
    for atom in get_set("modules", parent_dir=env.PORTMOD_LOCAL_DIR):
        mod = load_installed_mod(atom)
        for module_file in glob.glob(os.path.join(get_mod_path(mod), "*.pmodule")):
            module = __load_module_file(module_file, get_state(mod))
            module.add_parser(parsers)
            modules.append(module)
    return modules


def clean_up_modules(modules: Iterable[Module]):
    for module in modules:
        module.cleanup()


def require_module_updates():
    """
    Creates a file that indicates that modules need to be updated
    """
    open(os.path.join(env.PORTMOD_LOCAL_DIR, ".modules_need_updating"), "a").close()


def clear_module_updates():
    """Clears the file indicating that modules need updating"""
    path = os.path.join(env.PORTMOD_LOCAL_DIR, ".modules_need_updating")
    if os.path.exists(path):
        os.remove(path)


def modules_need_updating():
    """Returns true if changes have been made since the config was sorted"""
    return os.path.exists(os.path.join(env.PORTMOD_LOCAL_DIR, "sorting_incomplete"))


def get_redirections():
    """
    Iterates over all previously made file redirections and returns the (non-empty)
    results
    """
    protect_dir = os.path.join(env.CACHE_DIR, "cfg_protect")
    if os.path.exists(os.path.join(protect_dir, "cfg_protect.csv")):
        with open(os.path.join(protect_dir, "cfg_protect.csv"), "r") as file:
            reader = csv.reader(file)
            for row in reader:
                dst = row[0]
                src = row[1]

                if os.path.exists(src) and os.stat(src).st_size != 0:
                    yield src, dst


def clear_redirections():
    path = os.path.join(env.CACHE_DIR, "cfg_protect", "cfg_protect.csv")
    if os.path.exists(path):
        os.remove(path)
