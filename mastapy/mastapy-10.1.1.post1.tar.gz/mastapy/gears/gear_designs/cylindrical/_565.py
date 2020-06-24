'''_565.py

ScuffingTemperatureMethodsAGMA
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SCUFFING_TEMPERATURE_METHODS_AGMA = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ScuffingTemperatureMethodsAGMA')


__docformat__ = 'restructuredtext en'
__all__ = ('ScuffingTemperatureMethodsAGMA',)


class ScuffingTemperatureMethodsAGMA(Enum):
    '''ScuffingTemperatureMethodsAGMA

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SCUFFING_TEMPERATURE_METHODS_AGMA
    __hash__ = None

    USER_INPUT = 0
    FROM_TEST_GEARS = 1
    FROM_LUBRICANT_VISCOSITY = 2
