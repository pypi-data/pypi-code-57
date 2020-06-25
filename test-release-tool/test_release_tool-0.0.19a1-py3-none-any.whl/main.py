# -*- coding: utf-8 -*-
from . import __version__


def run():
    print("Hello from {} v{}".format(__name__, __version__))
    return 42
