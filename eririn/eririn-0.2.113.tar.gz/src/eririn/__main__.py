#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Usage: eririn <EXCELFILE> <FILE>...

where
    EXCELFILE is excelfile.xlsx
    FILE is input image file

Options:
  -h --help
  -v       verbose mode
"""

import os
import sys

from docopt import docopt
from . import conv as eririnlib


def main():
    arguments = docopt(__doc__)
    print(arguments)
    eririnlib.main(arguments)
