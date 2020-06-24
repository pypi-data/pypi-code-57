'''_1690.py

BearingProtectionLevel
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_PROTECTION_LEVEL = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingProtectionLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingProtectionLevel',)


class BearingProtectionLevel(Enum):
    '''BearingProtectionLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_PROTECTION_LEVEL
    __hash__ = None

    ALL_RESULTS_VISIBLE = 0
    INTERNAL_GEOMETRY_HIDDEN = 1
    INTERNAL_GEOMETRY_AND_ADVANCED_BEARING_RESULTS_HIDDEN = 2
