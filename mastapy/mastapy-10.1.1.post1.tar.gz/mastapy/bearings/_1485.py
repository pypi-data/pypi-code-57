'''_1485.py

RotationalDirections
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROTATIONAL_DIRECTIONS = python_net_import('SMT.MastaAPI.Bearings', 'RotationalDirections')


__docformat__ = 'restructuredtext en'
__all__ = ('RotationalDirections',)


class RotationalDirections(Enum):
    '''RotationalDirections

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ROTATIONAL_DIRECTIONS
    __hash__ = None

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    BIDIRECTIONAL = 2
