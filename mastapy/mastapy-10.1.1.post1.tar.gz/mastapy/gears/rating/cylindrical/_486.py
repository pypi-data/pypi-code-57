'''_486.py

GearBlankFactorCalculationOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GEAR_BLANK_FACTOR_CALCULATION_OPTIONS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'GearBlankFactorCalculationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearBlankFactorCalculationOptions',)


class GearBlankFactorCalculationOptions(Enum):
    '''GearBlankFactorCalculationOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _GEAR_BLANK_FACTOR_CALCULATION_OPTIONS
    __hash__ = None

    AVERAGE_VALUE = 0
    MINIMUM_VALUE = 1
