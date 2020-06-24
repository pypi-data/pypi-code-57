'''_1480.py

RollerBearingProfileTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING_PROFILE_TYPES = python_net_import('SMT.MastaAPI.Bearings', 'RollerBearingProfileTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearingProfileTypes',)


class RollerBearingProfileTypes(Enum):
    '''RollerBearingProfileTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ROLLER_BEARING_PROFILE_TYPES
    __hash__ = None

    NONE = 0
    LUNDBERG = 1
    DIN_LUNDBERG = 2
    CROWNED = 3
    JOHNS_GOHAR = 4
    USERSPECIFIED = 5
    CONICAL = 6
