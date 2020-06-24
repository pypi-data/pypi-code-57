'''_1691.py

BearingTypeExtraInformation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_TYPE_EXTRA_INFORMATION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingTypeExtraInformation')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingTypeExtraInformation',)


class BearingTypeExtraInformation(Enum):
    '''BearingTypeExtraInformation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_TYPE_EXTRA_INFORMATION
    __hash__ = None

    NONE = 0
    SKF_EXPLORER = 1
    XLIFE_PERFORMANCE = 2
    GENERATION_C = 4
