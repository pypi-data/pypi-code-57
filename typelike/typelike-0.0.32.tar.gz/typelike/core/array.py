"""
array.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .any import AnyLike

from abc import ABCMeta
import numpy as np
import pandas as pd


# ArrayLike class
class ArrayLike(AnyLike, metaclass=ABCMeta):
    """
    Something that is ``ArrayLike`` is something that can be coerced into a numpy.ndarray. This includes lists,
    sets, tuples, numpy.ndarray, pandas.Series, and pandas.DataFrame.

    Note: this class is not implemented. Don't create an instance, because it doesn't do anything.
    """

    # Needed to trick PyCharm
    # noinspection PyMissingConstructor
    def __init__(self):
        self.shape = None
        raise NotImplementedError


# Register subclasses
ArrayLike.register(list)
ArrayLike.register(set)
ArrayLike.register(tuple)
ArrayLike.register(np.ndarray)  # TODO is there a way to specify only 1D numpy arrays?
ArrayLike.register(pd.Series)
ArrayLike.register(pd.DataFrame)

AnyLike.register(ArrayLike)
