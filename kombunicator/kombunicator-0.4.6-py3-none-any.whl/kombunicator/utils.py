#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 12.06.20
@author: eisenmenger
"""

import pathlib
import re


def getter_setter(func):
    # from the awesome Ruud van der Ham
    return property(func, func)


def get_version(*, file_name: str, version_string: str) -> str:
    pattern = fr'({version_string})=(\d{{1,3}}.\d{{1,3}}.\d{{1,3}})'
    version = '0.0.1'
    release_info_file = pathlib.Path(file_name)
    if release_info_file.exists():
        with release_info_file.open('r') as file:
            try:
                version = re.findall(pattern, file.read())[-1][-1]
            except IndexError:
                pass  # raising exception here seems not really necessary
    return version
