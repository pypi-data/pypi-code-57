'''_1760.py

SleeveType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SLEEVE_TYPE = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'SleeveType')


__docformat__ = 'restructuredtext en'
__all__ = ('SleeveType',)


class SleeveType(Enum):
    '''SleeveType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SLEEVE_TYPE

    __hash__ = None

    NONE = 0
    WITHDRAWAL = 1
    ADAPTER = 2
