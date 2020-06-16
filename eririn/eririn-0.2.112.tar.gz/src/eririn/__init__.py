#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docopt import docopt
from . import conv as eririnlib
from . import __main__ as mainmain

def maineririn():
    arguments = docopt(mainmain.__doc__)
    print(arguments)
    eririnlib.main(arguments)
