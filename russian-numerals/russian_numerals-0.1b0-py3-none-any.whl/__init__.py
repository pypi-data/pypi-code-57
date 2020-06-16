# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#

from .handlers import (
    NumberToWords, NumberToRoubles, NumberToTons, NumberToKilograms,
    TextToNumbers,
)

__all__ = [
    'NumberToWords', 'NumberToRoubles', 'NumberToTons', 'NumberToKilograms',
    'TextToNumbers', 'HANDLERS', 'prepare',
]

HANDLERS = {
    'words': NumberToWords,
    'roubles': NumberToRoubles,
    'tons': NumberToTons,
    'kilograms': NumberToKilograms,
    'numbers': TextToNumbers,
}

# The version (X, Y, Z, R, N) builds by next rules:
# Variables X, Y, Z & N must be integers. R - can be 'alpha', 'beta' 'rc' or
# 'final' string. R == 'alpha' and N > 0 it is pre-alpha release.
# version = X.Y[.Z]
# subversion = .devN - for pre-alpha releases
#            | {a|b|c}N - for 'alpha', 'beta' and 'rc' releases
# subversion is not exists for 'final' release.
VERSION = (0, 1, 0, 'beta', 0)


def get_version():
    version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if version[2] == 0 else 3
    major = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        sub = '.dev'
    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return str(major + sub)


def prepare(value, handler=None):
    """Короткий метод для обработки одного значения."""
    if handler:
        handler = HANDLERS[handler]
    else:
        # Автоматическое определение обработчика.
        try:
            float(value)
        except ValueError:
            handler = TextToNumbers
        else:
            handler = NumberToWords
    return handler().prepare(value)
