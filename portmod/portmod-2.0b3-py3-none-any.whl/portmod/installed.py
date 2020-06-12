# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Generator, Tuple
from .repo.loader import load_all_installed
from .repo.usestr import check_required_use
from .pybuild import Pybuild, InstallDir, File


def get_installed_files(
    file_type: str,
) -> Generator[Tuple[Pybuild, InstallDir, File], None, None]:
    """Returns a generator over all files of a given type that are currently installed"""
    for mod in load_all_installed(flat=True):
        for install in mod.INSTALL_DIRS:
            if check_required_use(
                install.REQUIRED_USE, mod.INSTALLED_USE, mod.valid_use
            ):
                for file in install.__dict__.get(file_type, []):
                    if check_required_use(
                        file.REQUIRED_USE, mod.INSTALLED_USE, mod.valid_use
                    ):
                        yield mod, install, file
