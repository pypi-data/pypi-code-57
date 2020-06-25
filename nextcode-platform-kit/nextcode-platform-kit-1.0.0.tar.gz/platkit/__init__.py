#!/usr/bin/env python

import os


def get_version():
    version_filename = os.path.join(os.path.dirname(__file__), "VERSION")
    with open(version_filename) as f:
        return f.read().strip()


__version__ = get_version()
