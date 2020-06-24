'''_326.py

WormType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WORM_TYPE = python_net_import('SMT.MastaAPI.Gears', 'WormType')


__docformat__ = 'restructuredtext en'
__all__ = ('WormType',)


class WormType(Enum):
    '''WormType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WORM_TYPE
    __hash__ = None

    ZA = 0
    ZN = 1
    ZI = 2
    ZK = 3
