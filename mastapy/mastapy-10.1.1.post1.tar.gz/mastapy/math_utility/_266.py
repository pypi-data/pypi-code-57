'''_266.py

DataPrecision
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DATA_PRECISION = python_net_import('SMT.MastaAPI.MathUtility', 'DataPrecision')


__docformat__ = 'restructuredtext en'
__all__ = ('DataPrecision',)


class DataPrecision(Enum):
    '''DataPrecision

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _DATA_PRECISION
    __hash__ = None

    SINGLE = 0
    DOUBLE = 1
