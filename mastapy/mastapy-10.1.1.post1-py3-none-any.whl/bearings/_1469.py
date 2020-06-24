'''_1469.py

BearingRow
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings', 'BearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRow',)


class BearingRow(Enum):
    '''BearingRow

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_ROW
    __hash__ = None

    LEFT = 0
    RIGHT = 1
    SINGLE = 2
