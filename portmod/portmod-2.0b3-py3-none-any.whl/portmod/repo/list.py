# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for reading from list files"""

import os
from typing import List


def read_list(listpath: str) -> List[str]:
    """Reads the given list file and returns its contents"""
    with open(listpath, mode="r") as list_file:
        return [line.strip() for line in list_file.read().splitlines() if line]


def add_list(listpath: str, entry: str):
    """Appends the given value to the list file"""
    os.makedirs(os.path.dirname(listpath), exist_ok=True)
    with open(listpath, mode="a") as list_file:
        print(entry, file=list_file)
