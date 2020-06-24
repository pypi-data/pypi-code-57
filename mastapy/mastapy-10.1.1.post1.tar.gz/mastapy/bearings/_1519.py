'''_1519.py

JournalOilFeedType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_JOURNAL_OIL_FEED_TYPE = python_net_import('SMT.MastaAPI.Bearings', 'JournalOilFeedType')


__docformat__ = 'restructuredtext en'
__all__ = ('JournalOilFeedType',)


class JournalOilFeedType(Enum):
    '''JournalOilFeedType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _JOURNAL_OIL_FEED_TYPE

    __hash__ = None

    AXIAL_GROOVE = 0
    AXIAL_HOLE = 1
    CIRCUMFERENTIAL_GROOVE = 2
