import time
import os
import importlib


def import_module(module):
    """Import module from string"""
    parts = module.split('.')
    path = '.'.join(parts[0:-1])
    name = ''.join(parts[-1:])
    return (getattr(importlib.import_module(path), name), name, path)


def find_base_path(file):
    """
    Finds app base path relative to some __file__ in the app
    """
    count = 0
    path=os.path.dirname(os.path.realpath(file))
    while count < 50:
        if (
            os.path.exists(os.path.realpath(path + '/uvicorex')) or
            os.path.exists(os.path.realpath(path + '/setup.py')) or
            os.path.exists(os.path.realpath(path + '/.env'))
        ):
            return os.path.realpath(path)
        else:
            path = os.path.realpath(path + '/../')
        count += 1
    exit("Could not find base path")
