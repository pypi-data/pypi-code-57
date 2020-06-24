'''_1478.py

OuterRingMounting
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_OUTER_RING_MOUNTING = python_net_import('SMT.MastaAPI.Bearings', 'OuterRingMounting')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterRingMounting',)


class OuterRingMounting(Enum):
    '''OuterRingMounting

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _OUTER_RING_MOUNTING
    __hash__ = None

    STANDARD = 0
    SPHERICAL = 1
