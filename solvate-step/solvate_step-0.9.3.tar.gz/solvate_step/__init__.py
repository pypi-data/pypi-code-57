# -*- coding: utf-8 -*-

"""
solvate_step
A step for solvating the system using Packmol
"""

# Bring up the classes so that they appear to be directly in
# the solvate_step package.

from solvate_step.solvate import Solvate  # noqa: F401
from solvate_step.solvate_parameters import SolvateParameters  # noqa: F401
from solvate_step.solvate_step import SolvateStep  # noqa: F401
from solvate_step.tk_solvate import TkSolvate  # noqa: F401

# Handle versioneer
from ._version import get_versions
__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
