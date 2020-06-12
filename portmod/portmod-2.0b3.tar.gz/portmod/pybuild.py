# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import AbstractSet, Dict, List, Optional, Set, Tuple

import os
import lzma
import json
import hashlib
import logging
from functools import lru_cache
from portmod.repo.atom import Atom, FQAtom, QualifiedAtom
from portmod.globals import env
from .repo.usestr import use_reduce


class HashAlg:
    """
    Class for interacting with supported hash algorithms that can be used in manifests
    """

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return repr(self) < repr(other)


SHA512 = HashAlg("SHA512", hashlib.sha512)
MD5 = HashAlg("MD5", hashlib.md5)
HASH_ALGS = {"SHA512": SHA512, "MD5": MD5}


class Source:
    """Class used for storing information about download files"""

    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.hashes: Dict[HashAlg, str] = []
        self.size = None
        self.path = os.path.join(env.DOWNLOAD_DIR, name)
        basename, _ = os.path.splitext(name)
        # Hacky way to handle tar.etc having multiple extensions
        if basename.endswith("tar"):
            basename, _ = os.path.splitext(basename)

        self.basename = basename

    def manifest(self, size: int, hashes: Dict[HashAlg, str]):
        """Updates source to include values in manifest"""
        self.size = size
        self.hashes = hashes

    def __repr__(self):
        return self.url

    def __eq__(self, other):
        if not isinstance(other, Source):
            return False
        return self.url == other.url and self.name == other.name

    def __hash__(self):
        return hash((self.url, self.name, tuple(self.hashes)))


class InstallDir:
    def __init__(self, PATH, **kwargs):
        self.PATH = PATH
        self.REQUIRED_USE = kwargs.get("REQUIRED_USE", "")
        self.PATCHDIR = kwargs.get("PATCHDIR", ".")
        self.S = kwargs.get("S", None)
        source = kwargs.get("SOURCE", None)
        if self.S is None and source is not None:
            basename, _ = os.path.splitext(source)
            # Hacky way to handle tar.etc having multiple extensions
            if basename.endswith("tar"):
                basename, _ = os.path.splitext(basename)
            self.S = basename
            logging.warning(
                "InstallDir.SOURCE is deprecated. "
                "Please consider changing this to InstallDir.S: "
                f"{source}"
            )

        self.WHITELIST = kwargs.get("WHITELIST", None)
        self.BLACKLIST = kwargs.get("BLACKLIST", None)
        self.RENAME = kwargs.get("RENAME", None)
        self.DATA_OVERRIDES = kwargs.get("DATA_OVERRIDES", "")
        self.__keys__ = set()
        for key in kwargs:
            self.add_kwarg(key, kwargs[key])

    def add_kwarg(self, key, value):
        if isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict) and item.get("__type__") == "File":
                    file = dict(item)
                    file.pop("__type__", None)
                    new_value.append(File(**file))
                else:
                    new_value.append(item)
            value = new_value

        self.__dict__[key] = value
        self.__keys__.add(key)

    def get_files(self):
        """Generator function yielding file subattributes of the installdir"""
        for key in self.__dict__:
            if isinstance(getattr(self, key), list):
                for item in getattr(self, key):
                    if isinstance(item, File):
                        yield item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'InstallDir("{self.PATH}"' + separator + ", ".join(kvps) + ")"

    def to_cache(self):
        cache = {"PATH": self.PATH}
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, list):
                new = []
                for item in value:
                    if isinstance(item, File):
                        new.append(item.to_cache())
                    else:
                        new.append(item)
                value = new
            cache[key] = value

        return cache


class File:
    def __init__(self, NAME, **kwargs):
        self.__keys__ = set()
        self.NAME = NAME
        self.REQUIRED_USE = kwargs.get("REQUIRED_USE", "")
        self.OVERRIDES = kwargs.get("OVERRIDES", [])

        for key in kwargs:
            self.add_kwarg(key, kwargs[key])

    def add_kwarg(self, key, value):
        self.__dict__[key] = value
        self.__keys__.add(key)

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'File("{self.NAME}"' + separator + ", ".join(kvps) + ")"

    def to_cache(self):
        cache = {"NAME": self.NAME}
        for key in self.__keys__:
            cache[key] = getattr(self, key)

        cache["__type__"] = "File"
        return cache


class Pybuild:
    """
    Interface describing the Pybuild Type
    Only describes elements that are cached.
    This class cannot be used to install/uninstall mods
    """

    ATOM: FQAtom
    RDEPEND: str
    DEPEND: str
    SRC_URI: str
    M: Atom
    MF: Atom
    MN: Atom
    CATEGORY: str
    MV: str
    MR: str
    MVR: str
    CMN: QualifiedAtom
    CM: QualifiedAtom
    REQUIRED_USE: str
    RESTRICT: str
    PROPERTIES: str
    IUSE_EFFECTIVE: Set[str]
    IUSE: Set[str]
    TEXTURE_SIZES: str
    DESC: str
    NAME: str
    HOMEPAGE: str
    LICENSE: str
    KEYWORDS: str
    REBUILD: str
    TIER: str
    FILE: str
    REPO: str
    INSTALLED: bool = False
    INSTALL_DIRS: List[InstallDir]
    DATA_OVERRIDES = ""

    def to_cache(self) -> Dict:
        cache = {}
        for key in [
            "RDEPEND",
            "DEPEND",
            "SRC_URI",
            "REQUIRED_USE",
            "RESTRICT",
            "PROPERTIES",
            "IUSE_EFFECTIVE",
            "IUSE",
            "TEXTURE_SIZES",
            "DESC",
            "NAME",
            "HOMEPAGE",
            "LICENSE",
            "KEYWORDS",
            "REBUILD",
            "TIER",
            "FILE",
            "REPO",
            "DATA_OVERRIDES",
        ]:
            cache[key] = getattr(self, key)

        cache["INSTALL_DIRS"] = [idir.to_cache() for idir in self.INSTALL_DIRS]
        return cache

    def __init__(self, cache: Dict, atom: FQAtom):
        # Note: mypy doesn't like how we coerce INSTALL_DIRS
        self.__dict__ = cache
        self.ATOM = atom
        self.M = Atom(atom.M)
        self.MF = Atom(atom.MF)
        self.MN = Atom(atom.MN)
        self.CATEGORY = atom.C
        self.MV = atom.MV
        self.MR = atom.MR or "r0"
        self.MVR = atom.MVR
        self.CMN = QualifiedAtom(atom.CMN)
        self.CM = QualifiedAtom(atom.CM)
        self.__ENV = None
        self.INSTALLED = False
        self.INSTALL_DIRS = [InstallDir(**idir) for idir in self.INSTALL_DIRS]  # type: ignore

    def valid_use(self, use: str) -> bool:
        """Returns true if the given flag is a valid use flag for this mod"""
        return use in self.IUSE_EFFECTIVE

    @lru_cache()
    def get_installed_env(self):
        """Returns a dictionary containing installed object values"""
        if not self.INSTALLED:
            raise Exception("Trying to get environment for mod that is not installed")

        path = os.path.join(os.path.dirname(self.FILE), "environment.xz")
        if os.path.exists(path):
            environment = lzma.LZMAFile(path)
            return json.load(environment)

        return {}

    def get_dir_path(self, install_dir: InstallDir) -> str:
        """Returns the installed path of the given InstallDir"""
        path = os.path.normpath(
            os.path.join(env.MOD_DIR, self.CATEGORY, self.MN, install_dir.PATCHDIR)
        )
        if os.path.islink(path):
            return os.readlink(path)
        else:
            return path

    def get_file_path(self, install_dir: InstallDir, esp: File) -> str:
        return os.path.join(self.get_dir_path(install_dir), esp.NAME)

    def __str__(self):
        return self.ATOM

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.FILE + ")"

    @lru_cache()
    def get_manifest(self):
        """Returns the manifest object for the mod's sources"""
        from .repo.manifest import get_manifest

        return get_manifest(self.FILE)

    def get_default_sources(self) -> List[Source]:
        """
        Returns a list of sources that are enabled
        with the current use configuration
        """
        return self.get_sources(*self.get_use())

    def get_sources(
        self,
        uselist: AbstractSet[str] = frozenset(),
        masklist: AbstractSet[str] = frozenset(),
        matchnone=False,
        matchall=False,
    ) -> List[Source]:
        """
        Returns a list of sources that are enabled using the given configuration
        """
        from portmod.repo.download import parse_arrow

        sourcestr = self.SRC_URI
        sources = use_reduce(
            sourcestr,
            uselist,
            masklist,
            is_valid_flag=self.valid_use,
            is_src_uri=True,
            flat=True,
            matchnone=matchnone,
            matchall=matchall,
        )
        grouped = parse_arrow(sources)

        manifest = self.get_manifest()

        for source in grouped:
            if manifest.get(source.name) is not None:
                m = manifest.get(source.name)
                source.manifest(m.SIZE, m.hashes)

        return grouped

    def get_use(self) -> Tuple[Set[str], Set[str]]:
        """Returns the use flag configuration for the mod"""
        from .repo.use import get_use

        return get_use(self)

    def parse_string(self, string, matchall=False):
        if not matchall:
            (enabled, disabled) = self.get_use()
        else:
            (enabled, disabled) = ({}, {})

        return use_reduce(
            self.RESTRICT,
            enabled,
            disabled,
            is_valid_flag=self.valid_use,
            flat=True,
            matchall=matchall,
        )

    def get_restrict(self, *, matchall=False):
        """Returns parsed tokens in RESTRICT using current use flags"""
        return self.parse_string(self.RESTRICT, matchall=matchall)

    def get_properties(self, *, matchall=False):
        """Returns parsed tokens in PROPERTIES using current use flags"""
        return self.parse_string(self.PROPERTIES, matchall=matchall)


# Class used for typing pybuilds, allowing more flexibility with
# the implementations. Implementations of this class (e.g. Pybuild1)
# should derive it, but build file Mod classes should derive one of
# the implementations. This should be used as the type for any function that
# handles Pybuild objects.
#
# This provides a mechanism for modifying the Pybuild format, as we can
# make changes to this interface, and update the implementations to conform
# to it while keeping their file structure the same, performing conversions
# of the data inside the init function.
class FullPybuild(Pybuild):
    """Interface describing the Pybuild Type"""

    TIER: str
    REPO_PATH: str
    __pybuild__: str

    # Variables defined during the install/removal process
    A: List[Source]  # List of enabled sources
    D: str  # Destination directory where the mod is to be installed
    FILESDIR: str  # Path of the directory containing additional repository files
    ROOT: str  # Path of the installed directory of the mod
    S: Optional[str]  # Primary directory during prepare and install operations:w
    T: str  # Path of temp directory
    UNFETCHED: List[Source]  # List of sources that need to be fetched
    USE: Set[str]  # Enabled use flags
    WORKDIR: str  # Path of the working directory

    def mod_nofetch(self):
        """
        Function to give user instructions on how to fetch a mod
        which cannot be fetched automatically
        """

    def mod_pretend(self):
        """May be used to carry out sanity checks early on in the install process"""

    def src_unpack(self):
        """Function used to unpack mod sources"""

    def src_prepare(self):
        """Function used to apply patches and configuration"""

    def src_install(self):
        """Function used to create the final install directory"""

    def mod_prerm(self):
        """Function called immediately before mod removal"""

    def mod_postinst(self):
        """Function called immediately after mod installation"""

    @staticmethod
    def execute(
        command: str, pipe_output: bool = False, err_on_stderr: bool = False
    ) -> Optional[str]:
        """Function pybuild files can use to execute native commands"""


class InstalledPybuild(Pybuild):
    """Interface describing the type of installed Pybuilds"""

    INSTALLED_USE: Set[str]

    def __init__(self, cache: Dict, atom: FQAtom):
        super().__init__(cache, atom)
        self.INSTALLED_USE = set(self.INSTALLED_USE)
        self.INSTALLED = True

    def to_cache(self) -> Dict:
        cache = Pybuild.to_cache(self)
        cache["INSTALLED_USE"] = self.INSTALLED_USE
        return cache


class FullInstalledPybuild(InstalledPybuild, FullPybuild):
    """Interface describing the type of installed Pybuilds"""

    INSTALLED_USE: Set[str]

    def get_installed_env(self):
        """Returns a dictionary containing installed object values"""
