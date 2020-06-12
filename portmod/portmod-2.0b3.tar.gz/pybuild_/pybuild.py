# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

# pylint: disable=no-member

from typing import Generator, Iterable, List, Tuple

import os
import shutil
import patoolib
import logging
from logging import info, warning
from git import Git
from pathlib import Path
from portmod.util import patch_dir
from portmod.repo.atom import Atom, FQAtom, InvalidAtom, QualifiedAtom
from portmod.repo.usestr import use_reduce, check_required_use
from portmod.repo.metadata import (
    get_global_use,
    get_mod_metadata,
    license_exists,
    get_use_expand,
    check_use_expand_flag,
)
from portmod.colour import blue, green, magenta
from portmod.pybuild import File, FullPybuild, InstallDir, Source
from portmod.io_guard import _check_call, IOType
from portmod.config import get_config
from portmod.repo.loader import load_mod


def warn(string):
    """Deprecated Warning function for pybuilds. Use Pybuild1.warn instead"""
    warning(string)


def apply_patch(patch: str):
    """Applies git patch using Git apply"""
    print(f"Applying {patch}...")
    _check_call(patch, IOType.Read)
    _check_call(os.curdir, IOType.Write)
    for line in Git().apply([patch, "--numstat"]).split("\n"):
        file = line.split()[2]
        _check_call(file, IOType.Read)
        _check_call(file, IOType.Write)
    print(Git().apply([patch, "--stat", "--apply"]))


class Pybuild1(FullPybuild):
    RDEPEND = ""
    DEPEND = ""
    DATA_OVERRIDES = ""
    IUSE = ""  # type: ignore
    TIER = "a"
    KEYWORDS = ""
    LICENSE = ""
    NAME = ""
    DESC = ""
    HOMEPAGE = ""
    REBUILD = ""
    RESTRICT = ""
    PROPERTIES = ""
    TEXTURE_SIZES = ""
    REQUIRED_USE = ""
    SRC_URI = ""
    __ENV = None
    PATCHES = ""
    S = None
    INSTALL_DIRS: List[InstallDir] = []

    def __init__(self):
        self._warnings = []
        self._info = []
        self.FILE = self.__class__.__pybuild__

        category = Path(self.FILE).resolve().parent.parent.name
        # Note: type will be fixed later by the loader and will become an FQAtom
        self.ATOM = Atom(  # type: ignore
            "{}/{}".format(category, os.path.basename(self.FILE)[: -len(".pybuild")])
        )

        self.REPO_PATH = str(Path(self.FILE).resolve().parent.parent.parent)
        repo_name_path = os.path.join(self.REPO_PATH, "profiles", "repo_name")
        if os.path.exists(repo_name_path):
            with open(repo_name_path, "r") as repo_file:
                self.REPO = repo_file.readlines()[0].rstrip()
            self.ATOM = FQAtom("{}::{}".format(self.ATOM, self.REPO))

        self.M = Atom(self.ATOM.M)
        self.MN = Atom(self.ATOM.MN)
        self.MV = self.ATOM.MV
        self.MF = Atom(self.ATOM.MF)
        self.MR = self.ATOM.MR or "r0"
        self.CATEGORY = self.ATOM.C
        self.R = self.ATOM.R
        self.CM = QualifiedAtom(self.ATOM.CM)
        self.CMN = QualifiedAtom(self.ATOM.CMN)
        self.MVR = self.ATOM.MVR

        self.IUSE_EFFECTIVE = set()

        # Turn strings of space-separated atoms into lists
        if type(self.RDEPEND) is not str:
            raise TypeError("RDEPEND must be a string")

        if type(self.DEPEND) is not str:
            raise TypeError("DEPEND must be a string")

        if type(self.SRC_URI) is not str:
            raise TypeError("SRC_URI must be a string")

        if type(self.DATA_OVERRIDES) is not str:
            raise TypeError("DATA_OVERRIDES must be a string")

        if type(self.IUSE) is str:
            self.IUSE = set(self.IUSE.split())  # type: ignore # pylint: disable=no-member
            self.IUSE_EFFECTIVE |= set([use.lstrip("+") for use in self.IUSE])
        else:
            raise TypeError("IUSE must be a space-separated list of use flags")

        if type(self.KEYWORDS) is str:
            self.KEYWORDS = set(self.KEYWORDS.split())  # type: ignore # pylint: disable=no-member
        else:
            raise TypeError("KEYWORDS must be a space-separated list of keywords")

        if type(self.TIER) is int:
            self.TIER = str(self.TIER)
        elif type(self.TIER) is not str:
            raise TypeError("TIER must be a integer or string containing 0-9 or z")

        if type(self.LICENSE) is not str:
            raise TypeError(
                "LICENSE must be a string containing a space separated list of licenses"
            )

        if type(self.RESTRICT) is not str:
            raise TypeError(
                "RESTRICT must be a string containing a space separated list"
            )

        if type(self.PROPERTIES) is not str:
            raise TypeError(
                "PROPERTIES must be a string containing a space separated list"
            )

        if type(self.TEXTURE_SIZES) is str:
            texture_sizes = use_reduce(self.TEXTURE_SIZES, matchall=True)
            self.IUSE_EFFECTIVE |= set(
                ["texture_size_{}".format(size) for size in texture_sizes]
            )
        else:
            raise TypeError(
                "TEXTURE_SIZES must be a string containing a space separated list of "
                "texture sizes"
            )

        all_sources = self.get_sources(matchall=True)

        for install in self.INSTALL_DIRS:
            if isinstance(install, InstallDir):
                if len(all_sources) > 0 and install.S is None:
                    if len(all_sources) == 1:
                        install.S = all_sources[0].basename
                    else:
                        raise Exception(
                            "InstallDir does not declare a source name but source "
                            "cannot be set automatically"
                        )
                elif not all_sources and install.S is None:
                    install.S = self.M
            else:
                raise TypeError(
                    "InstallDir {} should be of type InstallDir".format(install)
                )

    def src_prepare(self):
        if self.PATCHES:
            enabled, disabled = self.get_use()
            for patch in use_reduce(self.PATCHES, enabled, disabled, flat=True):
                path = os.path.join(self.FILESDIR, patch)
                apply_patch(path)

    def src_install(self):
        case_insensitive = get_config().get("CASE_INSENSITIVE_FILES", False)
        for install_dir in self.INSTALL_DIRS:
            if check_required_use(
                install_dir.REQUIRED_USE, self.get_use()[0], self.valid_use
            ):
                info(
                    'Installing directory "{}" into "{}"'.format(
                        magenta(os.path.join(install_dir.S, install_dir.PATH)),
                        magenta(install_dir.PATCHDIR),
                    )
                )
                source = os.path.normpath(
                    os.path.join(self.WORKDIR, install_dir.S, install_dir.PATH)
                )
                if install_dir.RENAME is None:
                    dest = os.path.normpath(os.path.join(self.D, install_dir.PATCHDIR))
                else:
                    dest = os.path.normpath(
                        os.path.join(
                            self.D,
                            os.path.join(install_dir.PATCHDIR, install_dir.RENAME),
                        )
                    )

                _check_call(source, IOType.Read)
                _check_call(dest, IOType.Read)
                _check_call(dest, IOType.Write)

                blacklist = list(install_dir.BLACKLIST or [])
                for file in install_dir.get_files():
                    # ignore files which will not be used
                    if not check_required_use(
                        file.REQUIRED_USE, self.get_use()[0], self.valid_use
                    ):
                        blacklist.append(file.NAME)

                if os.path.islink(source):
                    linkto = os.readlink(source)
                    if os.path.exists(dest):
                        os.rmdir(dest)
                    os.symlink(linkto, dest, True)
                elif install_dir.WHITELIST is not None:
                    for file in install_dir.WHITELIST:
                        src_path = os.path.join(source, file)
                        dst_path = os.path.join(dest, file)
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        if os.path.isdir(src_path):
                            patch_dir(
                                src_path, dst_path, case_insensitive=case_insensitive
                            )
                        else:
                            shutil.copy(src_path, dst_path)
                elif blacklist is not None:
                    patch_dir(
                        source,
                        dest,
                        ignore=lambda directory, contents: [
                            os.path.basename(file)
                            for file in blacklist
                            if os.path.normpath(
                                os.path.join(source, os.path.dirname(file))
                            )
                            == os.path.normpath(directory)
                        ],
                        case_insensitive=case_insensitive,
                    )
                else:
                    patch_dir(source, dest, case_insensitive=case_insensitive)
            else:
                print(
                    'Skipping directory "{}" due to unsatisfied use '
                    "requirements {}".format(
                        magenta(os.path.join(install_dir.S, install_dir.PATH)),
                        blue(install_dir.REQUIRED_USE),
                    )
                )

    def mod_postinst(self):
        pass

    def mod_prerm(self):
        pass

    def validate(self):
        IUSE_STRIP = set([use.lstrip("+") for use in self.IUSE])
        errors = []

        try:
            rdeps = use_reduce(self.RDEPEND, token_class=Atom, matchall=True, flat=True)
            deps = use_reduce(self.DEPEND, token_class=Atom, matchall=True, flat=True)
            overrides = use_reduce(
                self.DATA_OVERRIDES, token_class=Atom, matchall=True, flat=True
            )
            for atom in rdeps + deps:
                if isinstance(atom, Atom) and not load_mod(atom, repo_name=self.REPO):
                    errors.append(f"Dependency {atom} could not be found!")

            for atom in overrides:
                if isinstance(atom, Atom) and not load_mod(atom, repo_name=self.REPO):
                    errors.append(f"Data Override {atom} could not be found!")

            use_reduce(self.PATCHES, matchall=True)
        except InvalidAtom as e:
            errors.append("{}".format(e))
        except Exception as e:
            errors.append("{}".format(e))

        all_sources = self.get_sources(matchall=True)

        for install in self.INSTALL_DIRS:
            if not isinstance(install, InstallDir):
                errors.append(
                    'InstallDir "{}" must have type InstallDir'.format(install.PATH)
                )
                continue
            for file in install.get_files():
                if not isinstance(file, File):
                    errors.append('File "{}" must have type File'.format(file))
                    continue

                try:
                    check_required_use(file.REQUIRED_USE, set(), self.valid_use)
                except Exception as e:
                    errors.append("Error processing file {}: {}".format(file.NAME, e))

            try:
                check_required_use(install.REQUIRED_USE, set(), self.valid_use)
            except Exception as e:
                errors.append("Error processing dir {}: {}".format(install.PATH, e))

            if len(all_sources) > 0 and not any(
                [install.S == source.basename for source in all_sources]
            ):
                warning(
                    'A source matching the basename "{}" '
                    "was not declared in SRC_URI".format(install.S)
                )
                print([source.basename for source in all_sources])

            if install.WHITELIST is not None and type(install.WHITELIST) is not list:
                errors.append("WHITELIST {} must be a list".format(install.WHITELIST))
            elif install.WHITELIST is not None:
                for string in install.WHITELIST:
                    if type(string) is not str:
                        errors.append(
                            "{} in InstallDir WHITELIST is not a string".format(string)
                        )

            if install.BLACKLIST is not None and type(install.BLACKLIST) is not list:
                errors.append("BLACKLIST {} must be a list".format(install.BLACKLIST))
            elif install.BLACKLIST is not None:
                for string in install.BLACKLIST:
                    if type(string) is not str:
                        errors.append(
                            "{} in InstallDir BLACKLIST is not a string".format(string)
                        )

            if install.WHITELIST is not None and install.BLACKLIST is not None:
                errors.append("WHITELIST and BLACKLIST are mutually exclusive")

        global_use = get_global_use(self.REPO_PATH)
        metadata = get_mod_metadata(self)

        for use in IUSE_STRIP:
            if global_use.get(use) is None and (
                metadata is None or metadata.get("use", {}).get(use, None) is None
            ):
                valid = False
                # If the flag contains an underscore, it may be a USE_EXPAND flag
                if "_" in use:
                    for use_expand in get_use_expand(self.REPO_PATH):
                        length = len(use_expand) + 1  # Add one for underscore
                        if use.startswith(use_expand.lower()) and check_use_expand_flag(
                            self.REPO_PATH, use_expand, use[length:]
                        ):
                            valid = True
                            break

                if not valid:
                    errors.append(
                        'Use flag "{}" must be either a global use flag '
                        "or declared in metadata.yaml".format(use)
                    )

        for value in self.get_restrict(matchall=True):
            if value not in {"fetch", "mirror"}:
                errors.append(f"Unsupported restrict flag {value}")

        if not self.NAME or "FILLME" in self.NAME or len(self.NAME) == 0:
            errors.append("Please fill in the NAME field")
        if not self.DESC or "FILLME" in self.DESC or len(self.DESC) == 0:
            errors.append("Please fill in the DESC field")
        if not isinstance(self.HOMEPAGE, str) or "FILLME" in self.HOMEPAGE:
            errors.append("Please fill in the HOMEPAGE field")

        for license in use_reduce(self.LICENSE, flat=True, matchall=True):
            if license != "||" and not license_exists(self.REPO_PATH, license):
                errors.append(
                    "LICENSE {} does not exit! Please make sure that it named "
                    "correctly, or if it is a new License that it is added to "
                    "the licenses directory of the repository".format(license)
                )

        if not isinstance(self.PATCHES, str):
            errors.append("PATCHES must be a string")

        manifest = self.get_manifest()
        for source in self.get_sources(matchall=True):
            if manifest.get(source.name) is None:
                errors.append(f'Source "{source.name}" is not listed in the Manifest')

        if len(errors) > 0:
            raise Exception(
                "Pybuild {} contains the following errors:\n{}".format(
                    green(self.FILE), "\n".join(errors)
                )
            )

    def unpack(self, archives: Iterable[Source]):
        """
        Unpacks the given archive into the workdir
        """
        for archive in archives:
            archive_name, ext = os.path.splitext(os.path.basename(archive.name))
            # Hacky way to handle tar.etc having multiple extensions
            if archive_name.endswith("tar"):
                archive_name, _ = os.path.splitext(archive_name)
            outdir = os.path.join(self.WORKDIR, archive_name)
            os.makedirs(outdir)
            if logging.root.level >= logging.WARN:
                verbosity = -1
            else:
                verbosity = 0
            patoolib.extract_archive(
                archive.path, outdir=outdir, interactive=False, verbosity=verbosity
            )

    def src_unpack(self):
        """Unpacks archives into the WORKDIR"""
        self.unpack(self.A)

    def can_update_live(self):
        """
        Indicates whether or not a live mod can be updated.

        If the mod is a live mod and can be updated, return True
        Otherwise, return False
        """
        return False

    def execute(self, command):
        """
        Allows execution of arbitrary commands at runtime.
        Command is sandboxed with filesystem and network access depending on
        the context in which it is called
        """
        raise Exception(f"execute was called from an invalid context in {self.M}")

    def get_directories(self) -> Generator[InstallDir, None, None]:
        """
        Returns all enabled InstallDir objects in INSTALL_DIRS
        """
        for install_dir in self.INSTALL_DIRS:
            if check_required_use(
                install_dir.REQUIRED_USE, self.get_use()[0], self.valid_use
            ):
                yield install_dir

    def get_files(self, typ: str) -> Generator[Tuple[InstallDir, File], None, None]:
        """
        Returns all enabled files and their directories
        """
        for install_dir in self.get_directories():
            if hasattr(install_dir, typ):
                for file in getattr(install_dir, typ):
                    yield install_dir, file

    def warn(self, string: str):
        """
        Displays warning message both immediately, and in the summary after all
        transactions have been completed
        """
        self._warnings.append(string)
        warning(string)

    def info(self, string: str):
        """
        Displays info message both immediately, and in the summary after all
        transactions have been completed
        """
        self._info.append(string)
        info(string)
