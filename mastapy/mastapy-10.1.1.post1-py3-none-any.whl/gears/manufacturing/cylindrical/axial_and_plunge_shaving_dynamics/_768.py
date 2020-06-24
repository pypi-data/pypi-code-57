'''_768.py

ActiveProfileRangeCalculationSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ACTIVE_PROFILE_RANGE_CALCULATION_SOURCE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ActiveProfileRangeCalculationSource')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveProfileRangeCalculationSource',)


class ActiveProfileRangeCalculationSource(Enum):
    '''ActiveProfileRangeCalculationSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ACTIVE_PROFILE_RANGE_CALCULATION_SOURCE
    __hash__ = None

    DESIGNED_GEAR_WITHOUT_TOLERANCES = 0
    MANUFACTURED_GEAR_WITH_TOLERANCES = 1
