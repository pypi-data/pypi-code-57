'''_290.py

CentreDistanceChangeMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CENTRE_DISTANCE_CHANGE_METHOD = python_net_import('SMT.MastaAPI.Gears', 'CentreDistanceChangeMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('CentreDistanceChangeMethod',)


class CentreDistanceChangeMethod(Enum):
    '''CentreDistanceChangeMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CENTRE_DISTANCE_CHANGE_METHOD
    __hash__ = None

    AUTOMATIC = 0
    MANUAL = 1
