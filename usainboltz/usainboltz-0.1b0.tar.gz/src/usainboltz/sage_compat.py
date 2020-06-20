# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

"""Compatibility with Sage.

Within a sage environment, we use some sage functionnalities such as SageObject
in order to interact well with the sage ecosystem. Outside of sage, we implement
simplified versions of these tools to keep a similar behaviour.
"""

try:
    from sage.all import latex
    from sage.misc.fast_methods import Singleton

except ImportError:

    def latex(x):
        if hasattr(x, "_latex_"):
            return x._latex_()
        else:
            return str(x)

    class Singleton:
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = object.__new__(cls)
            return cls._instance
