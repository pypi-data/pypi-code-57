# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Importing values from this module fills them with information about the file
from which they were imported
This module should be removed from sys.modules prior to importing to ensure that
the cached version is not used instead.
"""
import os
from typing import Optional
from pathlib import Path
from portmod.repo.atom import QualifiedAtom
from portmod.repo.loader import get_enclosing_filename

CATEGORY: str
M: str
MF: str
MN: str
MV: str
MR: Optional[str]
MVR: str


def _get_modinfo():
    """Puts module information in the global scope so that it can be imported"""
    global M, MF, MN, MV, MR, MVR, CATEGORY
    filename = get_enclosing_filename()
    if filename is not None:
        CATEGORY = Path(filename).resolve().parent.parent.name
        atom = QualifiedAtom(
            "{}/{}".format(CATEGORY, os.path.basename(filename)[: -len(".pybuild")])
        )

        M = atom.M
        MF = atom.MF
        MN = atom.MN
        MV = atom.MV
        MR = atom.MR
        MVR = atom.MV
        if atom.MR is not None:
            MVR += "-" + atom.MR


_get_modinfo()
