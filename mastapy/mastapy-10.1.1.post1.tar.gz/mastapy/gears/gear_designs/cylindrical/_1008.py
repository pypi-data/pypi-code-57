'''_1008.py

SpurGearLoadSharingCodes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPUR_GEAR_LOAD_SHARING_CODES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'SpurGearLoadSharingCodes')


__docformat__ = 'restructuredtext en'
__all__ = ('SpurGearLoadSharingCodes',)


class SpurGearLoadSharingCodes(Enum):
    '''SpurGearLoadSharingCodes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPUR_GEAR_LOAD_SHARING_CODES
    __hash__ = None

    LOAD_AT_HPSTC = 0
    LOAD_AT_TIP = 1
