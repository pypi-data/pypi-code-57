# -*- coding: utf-8 -*-
"""compatibleversion module.

This module determines if a version is permitted by a specifier.
"""

from packaging.specifiers import SpecifierSet
from packaging.version import Version


__version__ = "0.2.8"


def check_version(version, specifier, allow_pre=True):
    """Check version against specifier to see if version is specified."""
    if not version or not specifier:
        print("Must provide a value for version and specifier")
        raise ValueError

    version_obj = Version(version)
    specifier_obj = SpecifierSet(specifier)
    if allow_pre:
        specifier_obj.prereleases = allow_pre

    if list(specifier_obj.filter([version_obj])):
        return True

    return False
