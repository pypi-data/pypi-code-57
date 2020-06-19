
# Copyright 2019-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Meta data
"""

import sys
import typing
import re

from importlib.metadata import version, requires, PackageNotFoundError


def print_requirements(file: typing.TextIO = None) -> None:
    """Print version information of installed dependences

     ``> python -m quicc.meta``

    Args:
        file: Output stream (Defaults to stdout)
    """
    name_width = 24
    versions = {}
    versions['quicc'] = version('quicc')
    versions['python'] = sys.version[0:5]

    for req in requires('quicc'):
        name = re.split('[; =><]', req)[0]
        try:
            versions[name] = version(name)
        except PackageNotFoundError:    # pragma: no cover
            pass

    print(file=file)
    print('# Quicc versions (> python -m quicc.meta)', file=file)
    for name, vers in versions.items():
        print(name.ljust(name_width), vers, file=file)
    print(file=file)


if __name__ == '__main__':
    print_requirements()
