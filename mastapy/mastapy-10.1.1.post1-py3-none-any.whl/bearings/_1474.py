'''_1474.py

HybridSteelAll
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HYBRID_STEEL_ALL = python_net_import('SMT.MastaAPI.Bearings', 'HybridSteelAll')


__docformat__ = 'restructuredtext en'
__all__ = ('HybridSteelAll',)


class HybridSteelAll(Enum):
    '''HybridSteelAll

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HYBRID_STEEL_ALL
    __hash__ = None

    ALL = 0
    STEEL = 1
    HYBRID = 2
