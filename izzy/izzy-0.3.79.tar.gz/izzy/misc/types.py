"""
arraylike.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""


from abc import ABCMeta
import numpy as np
import pandas as pd


# ArrayLike class
class ArrayLike(metaclass=ABCMeta):
    """
    Something that is ``ArrayLike`` is anything that can be coerced into a :func:`numpy.ndarray`. This includes lists,
    tuples, sets, :func:`pandas.Series`, :func:`pandas.DataFrame`, etc.

    Note: this class is not implemented. Don't create an instance, because it doesn't do anything.
    """

    # Needed to trick PyCharm
    def __init__(self, data):
        self.shape = None

    # Needed to trick PyCharm
    def __getitem__(self, item):
        raise NotImplementedError

    # Needed to trick PyCharm
    def __iter__(self):
        raise NotImplementedError

    # Needed to trick PyCharm
    def __len__(self):
        raise NotImplementedError

    # Register subclass as ArrayLike
    @classmethod
    def register(cls, subclass):
        """
        Registers a new subclass as ``ArrayLike``

        Parameters
        ----------
        subclass : class
            Subclass to register as ``ArrayLike``
        """

        # noinspection PyCallByClass
        ABCMeta.register(cls, subclass)


# Register subclasses
ArrayLike.register(list)
ArrayLike.register(set)
ArrayLike.register(tuple)
ArrayLike.register(np.ndarray)
ArrayLike.register(pd.Series)
ArrayLike.register(pd.DataFrame)


# NoneType
NoneType = type(None)

