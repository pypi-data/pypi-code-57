'''_1078.py

MaxMinMean
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MAX_MIN_MEAN = python_net_import('SMT.MastaAPI.MathUtility', 'MaxMinMean')


__docformat__ = 'restructuredtext en'
__all__ = ('MaxMinMean',)


class MaxMinMean(Enum):
    '''MaxMinMean

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _MAX_MIN_MEAN

    __hash__ = None

    MAX = 0
    MIN = 1
    MEAN = 2
