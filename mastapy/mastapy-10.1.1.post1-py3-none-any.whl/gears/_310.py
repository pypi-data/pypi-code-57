'''_310.py

MicropittingCoefficientOfFrictionCalculationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICROPITTING_COEFFICIENT_OF_FRICTION_CALCULATION_METHOD = python_net_import('SMT.MastaAPI.Gears', 'MicropittingCoefficientOfFrictionCalculationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('MicropittingCoefficientOfFrictionCalculationMethod',)


class MicropittingCoefficientOfFrictionCalculationMethod(Enum):
    '''MicropittingCoefficientOfFrictionCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MICROPITTING_COEFFICIENT_OF_FRICTION_CALCULATION_METHOD
    __hash__ = None

    CALCULATED_CONSTANT = 0
    VARIABLE_BENEDICT_AND_KELLEY = 1
