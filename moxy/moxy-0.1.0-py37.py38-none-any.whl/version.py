#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   moxy, 2020
#   Blake VandeMerwe
# <<

__version__ = (0, 1, 0)
VERSION = version_str = '.'.join(map(str, __version__))

__all__ = [
    '__version__',
    'VERSION',
    'version_str',
    'version_info',
]


def version_info() -> str:
    import sys
    import platform
    from pathlib import Path

    from .main import compiled

    info = {
        'moxy version': VERSION,
        'moxy compiled': compiled,
        'install path': Path(__file__).resolve().parent,
        'python version': sys.version,
        'platform': platform.platform(),
    }
    return '\n'.join('{:>30} {}'.format(k + ':', str(v).replace('\n', ' ')) for k, v in info.items())
