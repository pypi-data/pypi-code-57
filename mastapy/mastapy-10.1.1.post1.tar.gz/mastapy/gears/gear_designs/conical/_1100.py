'''_1100.py

TopremEntryType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TOPREM_ENTRY_TYPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'TopremEntryType')


__docformat__ = 'restructuredtext en'
__all__ = ('TopremEntryType',)


class TopremEntryType(Enum):
    '''TopremEntryType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TOPREM_ENTRY_TYPE
    __hash__ = None

    TOPREM_LETTER = 0
    VALUES = 1
