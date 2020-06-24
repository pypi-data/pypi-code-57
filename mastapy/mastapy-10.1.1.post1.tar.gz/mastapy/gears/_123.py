'''_123.py

ContactRatioDataSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_RATIO_DATA_SOURCE = python_net_import('SMT.MastaAPI.Gears', 'ContactRatioDataSource')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactRatioDataSource',)


class ContactRatioDataSource(Enum):
    '''ContactRatioDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CONTACT_RATIO_DATA_SOURCE

    __hash__ = None

    DESIGN = 0
    OPERATING = 1
