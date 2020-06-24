'''_1042.py

MeasuredMapDataTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MEASURED_MAP_DATA_TYPES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'MeasuredMapDataTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasuredMapDataTypes',)


class MeasuredMapDataTypes(Enum):
    '''MeasuredMapDataTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MEASURED_MAP_DATA_TYPES
    __hash__ = None

    MULTIPLE_PROFILES = 0
    MULTIPLE_PROFILES_ONE_LEAD = 1
    MULTIPLE_LEADS = 2
    MULTIPLE_LEADS_ONE_PROFILE = 3
