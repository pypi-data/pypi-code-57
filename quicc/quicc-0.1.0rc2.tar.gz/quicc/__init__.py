
# Copyright 2019-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.


from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:    # pragma: no cover
    # package is not installed
    __version__ = '?.?.?'
