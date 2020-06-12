# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Dict, Generator, List, Optional
import ast
import sys
import glob
import os
import traceback
import copyreg
import re
import json
import importlib
import importlib.util
import inspect
from logging import warning
from types import ModuleType
from RestrictedPython import (
    compile_restricted_exec,
    RestrictingNodeTransformer,
    safe_globals,
    limited_builtins,
)
from RestrictedPython.Guards import (
    safer_getattr,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
)
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from copy import deepcopy
from portmod.repo.atom import atom_sat
from portmod.globals import env, get_version
from portmod.repo.metadata import get_categories
from portmod.config import get_config
from .util import get_hash
from .metadata import get_masters, get_repo_name
from .atom import Atom, FQAtom
from ..pybuild import Pybuild, InstalledPybuild, FullPybuild
from ..repos import get_repo
from ..io_guard import _check_call, IOType
from .zopeguards import protected_inplacevar


# We store a cache of mods so that they are only loaded once
# when doing dependency resolution.
# Stores key-value pairs of the form (filename, Mod Object)
class Cache:
    _mods: Dict[str, Pybuild] = {}
    _cached_mods: Dict[str, Pybuild] = {}

    def __init__(self):
        self._mods = {}
        self._cached_mods = {}

    def clear(self):
        self._mods = {}
        self._cached_mods = {}

    def clear_path(self, path: str):
        if path in self._mods:
            del self._mods[path]

        if path in self._cached_mods:
            del self._cached_mods[path]


cache = Cache()


def clear_cache_for_path(path: str):
    """
    Clears the mod cache for the given path

    Should be called if a file is updated and may be accessed again before the program exits
    """
    global cache
    cache.clear_path(path)


WRAPPED_IMPORTS = {"filecmp", "os", "pwinreg", "sys", "shutil", "os.path", "chardet"}
WHITELISTED_IMPORTS = {
    "pybuild_",
    "pybuild_.modinfo",
    "pybuild_.safemodules",
    "re",
    "csv",
    "json",
    "typing",
    "fnmatch",
    "collections",
} | {"pybuild_.safemodules." + imp for imp in WRAPPED_IMPORTS}
MODULE_WRAPPED_IMPORTS = {"logging", "xml", "xml.dom", "xml.dom.minidom"}
MODULE_WHITELISTED_IMPORTS = {
    "configparser",
    "portmod",
    "portmod.installed",
    "portmod.repo",
    "portmod.config",
    "portmod.repo.usestr",
    "portmod.tsort",
    "portmod.vfs",
    "portmod.module_util",
} | {"pybuild_.safemodules." + imp for imp in MODULE_WRAPPED_IMPORTS}

ALLOWED_IMPORTS = WRAPPED_IMPORTS | WHITELISTED_IMPORTS


class SafeModule(ModuleType):
    def __init__(
        self,
        name,
        dictionary,
        cache=None,
        extra_whitelist=frozenset(),
        extra_wrapped=frozenset(),
    ):
        WHITELIST = WHITELISTED_IMPORTS | extra_whitelist
        super().__init__(name)
        self.__dict__.clear()
        if cache is None:
            cache = {}
        for key in dictionary:
            if (
                not isinstance(dictionary[key], ModuleType)
                or ".".join([name, key]) in WHITELIST
            ):
                if isinstance(dictionary[key], type):
                    try:

                        class Derived(dictionary[key]):
                            pass

                        self.__dict__[key] = Derived
                    except TypeError:
                        # If we can't derive it, skip it entirely.
                        # The user probably doesn't need this type
                        pass
                elif isinstance(dictionary[key], ModuleType):
                    self.__dict__[key] = SafeModule(
                        dictionary[key].__name__,
                        dictionary[key].__dict__,
                        cache,
                        extra_whitelist,
                    )
                elif name in cache and key in cache[name]:
                    self.__dict__[key] = cache[name][key]
                else:
                    try:
                        self.__dict__[key] = deepcopy(dictionary[key])
                    except TypeError:
                        # If we fail to copy it, just ignore it.
                        # It's probably not going to be needed by the user.
                        # It may on the other hand be needed by the module during
                        # execution as we may execute on the Safe Module.
                        # My apologies for the inconvenience
                        pass
        cache[name] = self.__dict__


def reduce_mod(m):
    if m.__name__ not in WHITELISTED_IMPORTS:
        return None.__class__, ()
    return SafeModule, (m.__name__, m.__dict__)


copyreg.pickle(ModuleType, reduce_mod)
copyreg.pickle(SafeModule, reduce_mod)


def safe_import(_cache=None, extra_whitelist=set(), local_module_name=None):
    WHITELIST = WHITELISTED_IMPORTS | extra_whitelist
    cache = _cache or {}
    # We store a deepcopy module cache at the pybuild level. I.e. pybuilds are isolated
    # from each other, but we don't have to recursively clone every module they use
    clone_cache = {}

    def _import_root(name, glob=None, loc=None, fromlist=(), level=0):
        def _import(name, glob=None, loc=None, fromlist=(), level=0):
            """
            Safe implementation of __import__ to use with RestrictedPython
            """
            if glob:
                if "__path__" in glob:  # glob contains a module
                    module_name = glob["__name__"]
                else:  # Glob is a file, we want its parent
                    module_name = glob["__name__"].rpartition(".")[0]

                absolute_name = importlib.util.resolve_name(
                    level * "." + name, module_name
                )
            else:
                absolute_name = importlib.util.resolve_name(level * "." + name, None)

            path = None
            if "." in absolute_name:
                parent_name, _, child_name = absolute_name.rpartition(".")
                parent_module = _import(parent_name)
                path = parent_module.__spec__.submodule_search_locations

            if absolute_name in cache:
                return cache[absolute_name]

            # Note: using our custom code for whitelisted files has unintended side effects,
            # so we just import normally. See #135.
            if absolute_name in WHITELIST:
                module = __import__(name, glob, loc, fromlist, level)
                if "." in absolute_name:
                    cache[absolute_name] = getattr(parent_module, child_name)
                else:
                    cache[absolute_name] = module
                return cache[absolute_name]

            if (
                absolute_name in WHITELIST
                or absolute_name.startswith("pyclass")
                or (
                    local_module_name
                    and (
                        absolute_name == local_module_name
                        or absolute_name.startswith(local_module_name + ".")
                    )
                )
            ):
                if (
                    absolute_name == "pyclass"
                    or absolute_name.startswith("pyclass.")
                    or (
                        local_module_name
                        and (
                            absolute_name == local_module_name
                            or absolute_name.startswith(local_module_name + ".")
                        )
                    )
                ):
                    spec = safe_find_spec(
                        absolute_name, path, cache, extra_whitelist, local_module_name
                    )
                    spec.loader = RestrictedLoader(
                        absolute_name, spec.origin, extra_whitelist, local_module_name
                    )
                    spec.loader.cache = cache
                    module = importlib.util.module_from_spec(spec)
                    __SAFE_MODULES[absolute_name] = module
                else:
                    spec = importlib.util.find_spec(absolute_name, path)
                    spec.loader = importlib.machinery.SourceFileLoader(
                        absolute_name, spec.origin
                    )
                    module = importlib.util.module_from_spec(spec)
                if path is not None:
                    setattr(parent_module, child_name, module)
                cache[absolute_name] = module
                module.__loader__.exec_module(module)
                return module

            raise Exception(f"Unable to load restricted module {absolute_name}")

        module = _import(name, glob, loc, fromlist, level)

        if glob:
            absolute_name = importlib.util.resolve_name(
                level * "." + name, glob["__name__"]
            )
        else:
            absolute_name = importlib.util.resolve_name(level * "." + name, None)

        importname = absolute_name.split(".")[0]
        toimport = SafeModule(
            importname, cache[importname].__dict__, clone_cache, extra_whitelist
        )
        for key in fromlist or []:
            setattr(toimport, key, getattr(module, key))
        return toimport

    return _import_root


# Default implementation to handle invalid pybuilds
class Mod:
    def __init__(self):
        raise Exception("Mod is not defined")


def _write_wrapper():
    # Construct the write wrapper class
    def _handler(secattr, error_msg):
        # Make a class method.
        def handler(self, *args):
            try:
                f = getattr(self.ob, secattr)
            except AttributeError:
                raise TypeError(error_msg)
            f(*args)

        return handler

    class Wrapper(object, metaclass=type):
        def __init__(self, ob):
            object.__getattribute__(self, "__dict__")["ob"] = ob

        __setitem__ = _handler(
            "__guarded_setitem__", "object does not support item or slice assignment"
        )

        __delitem__ = _handler(
            "__guarded_delitem__", "object does not support item or slice assignment"
        )

        __setattr__ = _handler(
            "__guarded_setattr__", "attribute-less object (assign or del)"
        )

        __delattr__ = _handler(
            "__guarded_delattr__", "attribute-less object (assign or del)"
        )

    return Wrapper


def write_guard():
    """
    Write guard that blocks modifications to modules
    """
    bannedtypes = {ModuleType}
    Wrapper = _write_wrapper()

    def guard(ob):
        if type(ob) in bannedtypes:
            return Wrapper(ob)
        else:
            return ob

    return guard


def safe_open(path, mode="r", *args, **kwargs):
    """
    Safe function for opening files that can be used by pybuilds
    """
    _check_call(path, IOType.Read)
    if "w" in mode or "+" in mode or "a" in mode or "x" in mode:
        _check_call(path, IOType.Write)

    if not re.match(r"[rwxabt\+]+", mode):
        raise Exception("Invalid mode string!")

    return open(path, mode, *args, **kwargs)


def safer_hasattr(obj, name):
    """
    Version of hasattr implemented using safet_getattr

    This doesn't really provide any extra security, but does mean that
    str.format, and attributes beginning with underscores, which are
    blocked by safer_getattr, return False rather than True
    """
    try:
        safer_getattr(obj, name)
    except (NotImplementedError, AttributeError):
        return False
    return True


def default_apply(func, *args, **kwargs):
    return func(*args, **kwargs)


SAFE_GLOBALS = deepcopy(safe_globals)
SAFE_GLOBALS.update(
    {
        "Mod": Mod,
        "__metaclass__": type,
        "_getattr_": safer_getattr,
        "_getitem_": default_guarded_getitem,
        "_write_": write_guard(),
        "_apply_": default_apply,
        "super": super,
        "_getiter_": default_guarded_getiter,
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_unpack_sequence_": guarded_unpack_sequence,
        "_inplacevar_": protected_inplacevar,
        "FileNotFoundError": FileNotFoundError,
    }
)


class PrintWrapper:
    def __init__(self, _getattr_=None):
        self.txt = []
        self._getattr_ = _getattr_

    def write(self, text):
        self.txt.append(text)

    def __call__(self):
        return "".join(self.txt)

    def _call_print(self, *objects, **kwargs):
        if kwargs.get("file", None) is None:
            kwargs["file"] = sys.stdout
        else:
            self._getattr_(kwargs["file"], "write")
        print(*objects, **kwargs)


SAFE_GLOBALS["__builtins__"].update(
    {
        "_print_": PrintWrapper,
        "open": safe_open,
        "set": set,
        "frozenset": frozenset,
        "hasattr": safer_hasattr,
        "getattr": safer_getattr,
        "next": next,
        "iter": iter,
        "filter": filter,
        "map": map,
        "max": max,
        "min": min,
        "dict": dict,
        "enumerate": enumerate,
        "sum": sum,
        "any": any,
        "all": all,
        "reversed": reversed,
        "sorted": sorted,
    }
)
SAFE_GLOBALS["__builtins__"].update(limited_builtins)


class Policy(RestrictingNodeTransformer):
    def visit_JoinedStr(self, node):
        return self.node_contents_visit(node)

    def visit_FormattedValue(self, node):
        return self.node_contents_visit(node)

    def visit_AnnAssign(self, node):
        return self.node_contents_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in WRAPPED_IMPORTS | MODULE_WRAPPED_IMPORTS:
                alias.asname = alias.asname or alias.name
                alias.name = "pybuild_.safemodules." + alias.name
            elif alias.name == "pybuild" or alias.name.startswith("pybuild."):
                alias.asname = alias.asname or alias.name
                alias.name = "pybuild_" + alias.name.split("pybuild")[1]
            elif alias.name.split(".")[0] == "portmod" and not is_module_scope():
                # TODO: Deprecate then remove this prior to v2.0
                # self.warn(
                #    node,
                #    "Importing from portmod is deprecated. "
                #    "This will break in a future release unless you install the "
                #    "updated version of this mod.",
                # )
                alias.asname = alias.asname or alias.name
                alias.name = "pybuild_" + alias.name.split("portmod")[1]
            elif (
                alias.name == "portmod.pybuild"
                or alias.name.startswith("portmod.pybuild.")
            ) and not is_module_scope():
                # TODO: Deprecate then remove this prior to v2.0
                # self.warn(
                #    node,
                #     "Importing from portmod.pybuild is deprecated. "
                #     "This will break in a future release unless you install the "
                #     "updated version of this mod.",
                # )
                alias.asname = alias.asname or alias.name
                alias.name = "pybuild_" + alias.name.split("portmod.pybuild")[1]

        return RestrictingNodeTransformer.visit_Import(self, node)

    def visit_ImportFrom(self, node):
        if node.module in WRAPPED_IMPORTS | MODULE_WRAPPED_IMPORTS:
            node.module = "pybuild_.safemodules." + node.module
        elif node.module == "pybuild" or node.module.startswith("pybuild."):
            node.module = "pybuild_" + node.module.split("pybuild")[1]
        elif node.module == "portmod" and not is_module_scope():
            # TODO: Deprecate then remove this prior to v2.0
            # self.warn(
            #     node,
            #     "Importing from portmod is deprecated. "
            #     "This will break in a future release unless you install the "
            #     "updated version of this mod.",
            # )
            node.module = "pybuild_"
        elif (
            node.module == "portmod.pybuild"
            or node.module.startswith("portmod.pybuild.")
        ) and not is_module_scope():
            # TODO: Deprecate then remove this prior to v2.0
            # self.warn(
            #     node,
            #     "Importing from portmod.pybuild is deprecated. "
            #     "This will break in a future release unless you install the "
            #     "updated version of this mod.",
            # )
            node.module = "pybuild_" + node.module.split("portmod.pybuild")[1]

        if (
            not node.module.startswith("pyclass.")
            and node.module != "pyclass"
            and node.module not in ALLOWED_IMPORTS
            and node.module not in MODULE_WHITELISTED_IMPORTS
            and node.level == 0
        ):
            raise Exception(f"Not allowed to import from {node.module}")
        # For pyclass, skip this restriction, since it will be loaded with
        # full restrictions in place. No unsafe modules will be available
        if (
            node.module != "pyclass"
            and not node.module.startswith("pyclass.")
            and node.level == 0
        ):
            module = importlib.import_module(node.module)
            for name in node.names:
                if isinstance(module.__dict__.get(name.name), type(importlib)):
                    self.error(
                        node, "Importing modules from other modules is forbidden"
                    )

        if node.module == "pybuild_.modinfo":
            del sys.modules[node.module]

        return RestrictingNodeTransformer.visit_ImportFrom(self, node)

    def visit_Name(self, node):
        if node.id == "__PERMS":
            self.error(node, "Declaring i/o permissions is not allowed in the sandbox")
        return RestrictingNodeTransformer.visit_Name(self, node)

    def visit_FunctionDef(self, node):
        node = RestrictingNodeTransformer.visit_FunctionDef(self, node)
        if node.name == "__init__":
            newnode = ast.parse("super().__init__()").body[0]
            newnode.lineno = node.lineno
            newnode.col_offset = node.col_offset
            node.body.insert(0, newnode)
        return node


class RestrictedLoader(importlib.machinery.SourceFileLoader):
    def __init__(self, abs_name, origin, extra_whitelist=[], local_module_name=None):
        super().__init__(abs_name, origin)
        self.extra_whitelist = extra_whitelist
        self.local_module_name = local_module_name

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(module.__file__, "r") as module_file:
            tmp_globals = deepcopy(SAFE_GLOBALS)
            tmp_globals["__builtins__"]["__import__"] = safe_import(
                self.__dict__.get("cache", None),
                self.extra_whitelist,
                self.local_module_name,
            )
            tmp_globals.update(module.__dict__)
            restricted_load(module_file.read(), module.__file__, tmp_globals)
            module.__dict__.update(tmp_globals)


def safe_find_spec(
    name, package=None, cache=None, extra_whitelist=[], local_module_name=None
):
    """
    Find a module's spec.
    Modified from importlib
    """

    def _find_spec(name, path, target=None):
        meta_path = sys.meta_path
        if meta_path is None:
            # PyImport_Cleanup() is running or has been called.
            raise ImportError("sys.meta_path is None, Python is likely shutting down")

        if not meta_path:
            warning("sys.meta_path is empty")

        for finder in meta_path:
            spec = None
            try:
                spec = finder.find_spec(name, path, target)
                if spec is not None:
                    return spec
            except AttributeError:
                loader = finder.find_module(name, path)
                if loader is not None:
                    spec = importlib.util.spec_from_loader(name, loader)
                    if spec is not None:
                        return spec
        else:
            return None

    fullname = (
        importlib.util.resolve_name(name, package) if name.startswith(".") else name
    )
    if fullname not in __SAFE_MODULES:
        parent_name = fullname.rpartition(".")[0]
        if parent_name:
            if parent_name in __SAFE_MODULES:
                parent = __SAFE_MODULES[parent_name]
            else:
                parent = safe_import(cache, extra_whitelist, local_module_name,)(
                    parent_name, glob=globals(), fromlist=["__path__"]
                )
            try:
                parent_path = parent.__path__
            except AttributeError as error:
                raise ModuleNotFoundError(
                    f"__path__ attribute not found on {parent_name!r} "
                    f"while trying to find {fullname!r}",
                    name=fullname,
                ) from error
        else:
            parent_path = None
        return _find_spec(fullname, parent_path or package)

    module = __SAFE_MODULES[fullname]
    if module is None:
        return None
    try:
        spec = module.__spec__
    except AttributeError:
        raise ValueError("{}.__spec__ is not set".format(name)) from None
    else:
        if spec is None:
            raise ValueError("{}.__spec__ is None".format(name))
        return spec


__SAFE_MODULES: Dict[str, ModuleType] = {}


def restricted_load(code, filepath, _globals):
    if sys.platform == "win32":
        code = code.replace("\\", "\\\\")
    byte_code, errors, warnings, names = compile_restricted_exec(
        code, filename=filepath, policy=Policy
    )
    if errors:
        raise SyntaxError(errors)
    seen = {}
    for message in [seen.setdefault(x, x) for x in warnings if x not in seen]:
        if not message.endswith("Prints, but never reads 'printed' variable."):
            warning(f"In file {filepath}: {message}")
    exec(byte_code, _globals, _globals)


def cache_valid(path: str) -> bool:
    """
    Determines if the cache file at the given path is valid

    Returns true if and only if the cache file at the given path exists,
    the version of portmod is the same as the version stored in the cache file
    and that all file hashes in the cache file are valid
    """
    if not os.path.exists(path):
        return False

    with open(path, "r") as cache_file:
        try:
            mod = json.load(cache_file)
        except Exception:
            return False

    if mod.get("__portmod_version__") != get_version():
        return False

    if not mod.get("__hashes__", []):
        return False

    for file, file_hash in mod.get("__hashes__"):
        if get_hash(file) != file_hash:
            return False

    return True


def create_cache_file(mod: FullPybuild):
    if mod.INSTALLED:
        repo = "installed"
    else:
        repo = mod.REPO

    dirname = os.path.join(env.PYBUILD_CACHE_DIR, repo, mod.CATEGORY)
    os.makedirs(dirname, exist_ok=True)
    path = os.path.join(dirname, mod.MF)

    # Don't create the cache file if there is an existing, valid, cache file
    if cache_valid(path):
        return

    with open(path, "w") as cache_file:
        # Serialize as best we can. Sets become lists and unknown objects are
        # just stringified
        def dumper(obj):
            if isinstance(obj, set):
                return list(obj)
            return "{}".format(obj)

        # Only include members declared in the Pybuild class.
        # Internal members should be ignored
        if mod.INSTALLED:
            dictionary = InstalledPybuild.to_cache(mod)
        else:
            dictionary = mod.to_cache()
        dictionary["__portmod_version__"] = get_version()
        for key in get_config()["CACHE_FIELDS"]:
            if hasattr(mod, key):
                dictionary[key] = getattr(mod, key)

        hashes = [(mod.FILE, get_hash(mod.FILE))]
        for super_cl in mod.__class__.mro():
            module = super_cl.__module__.split(".")
            # Note: All superclasses will be either in the pyclass directory,
            # portmod builtin superclasses, or builtin objects
            # We track v
            if module[0] != "pyclass":
                continue

            REPO_PATH = mod.REPO_PATH
            if mod.INSTALLED:
                REPO_PATH = get_repo(mod.REPO).location

            # Find path for pyclass module file
            filepath = os.path.join(REPO_PATH, *module) + ".py"
            dirpath = os.path.join(REPO_PATH, *module, "__init__.py")
            if os.path.exists(filepath):
                hashes.append((filepath, get_hash(filepath)))
                continue
            elif os.path.exists(dirpath):
                hashes.append((dirpath, get_hash(dirpath)))
                continue

            found = False
            for master in get_masters(REPO_PATH):
                filepath = os.path.join(master.location, *module) + ".py"
                dirpath = os.path.join(master.location, *module, "__init__.py")
                if os.path.exists(filepath):
                    hashes.append((filepath, get_hash(filepath)))
                    found = True
                    break
                elif os.path.exists(dirpath):
                    hashes.append((dirpath, get_hash(dirpath)))
                    found = True
                    break

            if not found:
                raise Exception(
                    f"Could not find path for module {super_cl.__module__} "
                    f"for mod {mod}"
                )

        dictionary["__hashes__"] = hashes

        json.dump(dictionary, cache_file, default=dumper, sort_keys=True)


def load_cache(path: str, installed: bool) -> Pybuild:
    repopath, filename = os.path.split(path)
    atom, _ = os.path.splitext(filename)
    repopath, MN = os.path.split(repopath)
    repopath, C = os.path.split(repopath)
    if installed:
        repo_name = "installed"
    else:
        repo_name = get_repo_name(repopath)
    cache_file = os.path.join(env.PYBUILD_CACHE_DIR, repo_name, C, atom)

    if not cache_valid(cache_file):
        create_cache_file(__load_mod_from_dict_cache(path, False, installed=installed))

    with open(cache_file, "r") as cache_file:
        mod = json.load(cache_file)
        mod["FILE"] = path
        mod["INSTALLED"] = installed

        if installed:
            return InstalledPybuild(
                mod, FQAtom(f'{C}/{atom}::{mod["REPO"]}::installed')
            )
        else:
            return Pybuild(mod, FQAtom(f"{C}/{atom}::{repo_name}"))


def __load_file(file):
    # Ensure that we never use the cached version of modinfo
    if "pybuild_.modinfo" in sys.modules:
        del sys.modules["pybuild_.modinfo"]

    filename, _ = os.path.splitext(os.path.basename(file))

    with open(file, "r") as module_file:
        code = module_file.read()
        tmp_globals = deepcopy(SAFE_GLOBALS)
        tmp_globals["__builtins__"]["__import__"] = safe_import()
        tmp_globals["__name__"] = filename
        restricted_load(code, file, tmp_globals)
        tmp_globals["Mod"].__pybuild__ = file
        mod = tmp_globals["Mod"]()

    mod.FILE = os.path.abspath(file)
    mod.INSTALLED = False
    return mod


def __load_module_file(file, state):
    """Loads a module file using the sandbox"""
    from portmod.modules import Module, ModuleFunction

    module_name = os.path.basename(os.path.dirname(file))
    filename, _ = os.path.splitext(os.path.basename(file))
    functions = []

    sys.path.append(os.path.dirname(os.path.dirname(file)))

    with open(file, "r") as module_file:
        code = module_file.read()
        tmp_globals = deepcopy(SAFE_GLOBALS)
        tmp_globals["__builtins__"]["__import__"] = safe_import(
            extra_whitelist=MODULE_WHITELISTED_IMPORTS,
            local_module_name=os.path.basename(os.path.dirname(file)),
        )
        tmp_globals["__name__"] = module_name + "." + filename
        restricted_load(code, file, tmp_globals)

        do_functions = {}
        describe_options = {}
        describe_parameters = {}
        for globname in tmp_globals:
            if globname.startswith("do_"):
                do_functions[re.sub("^do_", "", globname)] = tmp_globals[globname]
            match = re.match("^describe_(.*)_options$", globname)
            if match:
                describe_options[match.group(1)] = tmp_globals[globname]
            match = re.match("^describe_(.*)_parameters$", globname)
            if match:
                describe_parameters[match.group(1)] = tmp_globals[globname]

        functions = []
        for function in do_functions:
            functions.append(
                ModuleFunction(
                    function,
                    do_functions[function],
                    describe_options.get(function),
                    describe_parameters.get(function),
                    state,
                )
            )

        name = os.path.basename(file)
        name, _ = os.path.splitext(name)
        module = Module(
            name, tmp_globals["__doc__"], sorted(functions, key=lambda x: x.name), state
        )

    sys.path.pop()
    return module


def load_all_installed(*, flat=False, cached=True):
    """
    Returns every single installed mod in the form of a map from their simple mod name
    to their mod object
    """
    if flat:
        mods = set()
    else:
        mods = {}
    repo = env.INSTALLED_DB

    for path in glob.glob(os.path.join(repo, "*/*")):
        mod = __load_installed_mod(path, cached)
        if mod is not None:
            if flat:
                mods.add(mod)
            else:
                if mods.get(mod.MN) is None:
                    mods[mod.MN] = [mod]
                else:
                    mods[mod.MN].append(mod)
    return mods


def __load_mod_from_dict_cache(file: str, cached: bool, *, installed=False) -> Pybuild:
    global cache
    if cached:
        dictionary = cache._cached_mods
    else:
        dictionary = cache._mods

    if dictionary.get(file, False):
        return dictionary[file]
    elif cached:
        mod = load_cache(file, installed)
        dictionary[file] = mod
        return mod
    else:
        mod = __load_file(file)
        mod.INSTALLED = installed
        if installed:
            parent = os.path.dirname(file)
            with open(os.path.join(parent, "REPO"), "r") as repo_file:
                mod.REPO = repo_file.readlines()[0].rstrip()
                mod.ATOM = Atom(mod.ATOM + "::" + mod.REPO + "::installed")
            with open(os.path.join(parent, "USE"), "r") as use_file:
                mod.INSTALLED_USE = set(use_file.readlines()[0].split())

        dictionary[file] = mod

        create_cache_file(mod)
        return mod


def __safe_load(user_function):
    """
    Decorator that makes a function return None if it would otherwise raise an exception
    """

    def decorating_function(name, *args, **kwargs):
        try:
            return user_function(name, *args, **kwargs)
        except Exception as e:
            warning(e)
            if env.DEBUG:
                traceback.print_exc()
            warning('Could not load pybuild "{}"'.format(name))
            if env.ALLOW_LOAD_ERROR:
                return None
            raise e

    return decorating_function


@__safe_load
def full_load_file(path, *, installed=False) -> FullPybuild:
    if installed:
        return __load_installed_mod(os.path.dirname(path), False)
    else:
        return __load_file(path)


@__safe_load
def full_load_mod(mod: Pybuild) -> FullPybuild:
    if mod.INSTALLED:
        return __load_installed_mod(os.path.dirname(mod.FILE), False)
    else:
        return __load_mod_from_dict_cache(mod.FILE, False)


def __load_installed_mod(path: str, cached: bool) -> Optional[InstalledPybuild]:
    if os.path.exists(path):
        files = glob.glob(os.path.join(path, "*.pybuild"))
        if len(files) > 1:
            atom = Atom(
                os.path.basename(os.path.dirname(files[0]))
                + "/"
                + os.path.basename(files[0].rstrip(".pybuild"))
            )
            raise Exception('Multiple versions of mod "{}" installed!'.format(atom))
        elif len(files) == 0:
            return None

        for file in files:
            mod = __load_mod_from_dict_cache(file, cached, installed=True)

            return mod
    return None


@__safe_load
def load_installed_mod(atom: Atom) -> Optional[InstalledPybuild]:
    """Loads mods from the installed database"""
    repo = env.INSTALLED_DB

    path = None
    if atom.C:
        path = os.path.join(repo, atom.C, atom.MN)
    else:
        for dirname in glob.glob(os.path.join(repo, "*")):
            path = os.path.join(repo, dirname, atom.MN)
            if os.path.exists(path):
                break

    if path is not None:
        mod = __load_installed_mod(path, True)
    else:
        return None

    if mod is not None and atom_sat(mod.ATOM, atom):
        return mod

    return None


def iterate_pybuilds(
    atom: Optional[Atom] = None, repo_name: Optional[str] = None
) -> Generator[str, None, None]:
    path = None
    repos = env.REPOS
    if repo_name is not None:
        repo = get_repo(repo_name)
        repos = [repo]
        for master in get_masters(repo.location):
            yield from iterate_pybuilds(atom, master)

    for repo in repos:
        if not os.path.exists(repo.location):
            warning(
                "Repository {} does not exist at configured location {}".format(
                    repo.name, repo.location
                )
            )
            print(
                'You might need to run "omwmerge --sync" if this is a remote repository'
            )

        if atom:
            if atom.C:
                path = os.path.join(repo.location, atom.C, atom.MN)
                if path is not None and os.path.exists(path):
                    for file in glob.glob(os.path.join(path, "*.pybuild")):
                        yield file
            else:
                for category in get_categories(repo.location):
                    path = os.path.join(repo.location, category, atom.MN)

                    if path is not None and os.path.exists(path):
                        for file in glob.glob(os.path.join(path, "*.pybuild")):
                            yield file
        else:
            for file in glob.glob(os.path.join(repo.location, "*", "*", "*.pybuild")):
                yield file


def load_mod_fq(atom: FQAtom) -> Pybuild:
    """
    Loads mod matching fully qualified atom.

    If mod cannot be found, or multiple mods match the atom, raises and exception
    """
    if atom.R.endswith("::installed"):
        return load_installed_mod(atom)

    mods: List[Pybuild] = []
    for file in iterate_pybuilds(atom):
        mod = __safe_load(__load_mod_from_dict_cache)(file, True, installed=False)
        if mod is None:
            continue

        if mod.ATOM == atom:
            mods.append(mod)

    if len(mods) > 1:
        raise Exception(
            f"FQ Atom {atom} is ambiguous, and matches all of\n"
            + ", ".join([f"{mod}" for mod in mods])
        )
    elif len(mods) == 1:
        return mods[0]

    raise Exception(f"Could not find mod {atom}")


def load_mod(atom: Atom, *, repo_name: Optional[str] = None) -> List[Pybuild]:
    """
    Loads all mods matching the given atom
    There may be multiple versions in different repos,
    as well versions with different version or release numbers

    :param atom: Mod atom to load.
    :param repo_name: If present, the name of the repository tree to search.
                      The masters of the given repository will also be searched.
    """
    mods = []

    for file in iterate_pybuilds(atom, repo_name):
        mod = __safe_load(__load_mod_from_dict_cache)(file, True, installed=False)

        if mod is None:
            continue

        if atom_sat(mod.ATOM, atom):
            mods.append(mod)

    if repo_name is None:
        installed = load_installed_mod(atom)
        if installed:
            mods.append(installed)

    return mods


def load_all():
    for file in iterate_pybuilds():
        mod = __safe_load(__load_mod_from_dict_cache)(file, True, installed=False)
        if mod is None:
            continue

        yield mod


def is_module_scope() -> bool:
    """
    Returns true if and only if this was called during the execution of a module file
    """
    for i in inspect.stack(0):
        if i.filename.endswith(".pmodule"):
            return True
    return False


def get_enclosing_filename() -> Optional[str]:
    """
    Returns the pybuild whose scope we are executing in

    Must be called form within the scope of execution of a pybuild file
    """
    filename = None
    for i in inspect.stack(0):
        if i.filename.endswith(".pybuild") or i.filename.endswith(".pmodule"):
            filename = i.filename
    return filename
