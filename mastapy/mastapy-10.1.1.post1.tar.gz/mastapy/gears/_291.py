'''_291.py

CoefficientOfFrictionCalculationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COEFFICIENT_OF_FRICTION_CALCULATION_METHOD = python_net_import('SMT.MastaAPI.Gears', 'CoefficientOfFrictionCalculationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('CoefficientOfFrictionCalculationMethod',)


class CoefficientOfFrictionCalculationMethod(Enum):
    '''CoefficientOfFrictionCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _COEFFICIENT_OF_FRICTION_CALCULATION_METHOD
    __hash__ = None

    ISOTR_1417912001 = 0
    ISOTR_1417912001_WITH_SURFACE_ROUGHNESS_PARAMETER = 1
    ISOTR_1417922001 = 2
    ISOTR_1417922001_MARTINS_ET_AL = 3
    DROZDOV_AND_GAVRIKOV = 4
    ODONOGHUE_AND_CAMERON = 5
    MISHARIN = 6
    ISO_TC60 = 7
    BENEDICT_AND_KELLEY = 8
    USER_SPECIFIED = 9
