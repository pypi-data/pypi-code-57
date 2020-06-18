#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   moxy, 2020
#   Blake VandeMerwe
# <<

try:
    import cython  # type: ignore
except ImportError:
    compiled: bool = False
else:  # pragma: no cover
    try:
        compiled = cython.compiled
    except AttributeError:
        compiled = False


__all__ = [
    'compiled',
]
