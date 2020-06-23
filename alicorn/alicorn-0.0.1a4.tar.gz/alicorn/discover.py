#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
#  Discovers service modules and automatically imports them
import pkgutil
import importlib


def auto_discover(locations=None, name='service'):
    """Automatically import modules that match the given base location and name"""
    if not locations:
        locations = ['.']

    # Iterate the modules in the given locations looking for name
    for module in pkgutil.iter_modules(locations):
        if module.ispkg and pkgutil.find_loader(f'{module.name}.{name}'):
            importlib.import_module(f'{module.name}.{name}')
