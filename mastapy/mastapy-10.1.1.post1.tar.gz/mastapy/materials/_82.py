'''_82.py

PressureViscosityCoefficientMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PRESSURE_VISCOSITY_COEFFICIENT_METHOD = python_net_import('SMT.MastaAPI.Materials', 'PressureViscosityCoefficientMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('PressureViscosityCoefficientMethod',)


class PressureViscosityCoefficientMethod(Enum):
    '''PressureViscosityCoefficientMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _PRESSURE_VISCOSITY_COEFFICIENT_METHOD

    __hash__ = None

    TEMPERATURE_INDEPENDENT_VALUE = 0
    TEMPERATURE_AND_VALUE_AT_TEMPERATURE_SPECIFIED = 1
    SPECIFY_K_AND_S = 2
