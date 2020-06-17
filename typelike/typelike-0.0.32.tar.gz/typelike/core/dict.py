"""
dict.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .any import AnyLike

from abc import ABCMeta
import numpy as np
import pandas as pd


# DictLike class
class DictLike(AnyLike, metaclass=ABCMeta):
    """
    Something that is ``DictLike`` is something that can operate as a dictionary.

    Note: this class is not implemented. Don't create an instance, because it doesn't do anything.
    """

    # Needed to trick PyCharm
    # noinspection PyMissingConstructor
    def __init__(self):
        raise NotImplementedError


# Register subclasses
DictLike.register(dict)
DictLike.register(pd.DataFrame)
DictLike.register(pd.Series)

AnyLike.register(DictLike)
