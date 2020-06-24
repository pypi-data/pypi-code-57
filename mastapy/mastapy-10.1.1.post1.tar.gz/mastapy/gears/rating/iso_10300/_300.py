'''_300.py

PittingFactorCalculationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PITTING_FACTOR_CALCULATION_METHOD = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'PittingFactorCalculationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('PittingFactorCalculationMethod',)


class PittingFactorCalculationMethod(Enum):
    '''PittingFactorCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PITTING_FACTOR_CALCULATION_METHOD
    __hash__ = None

    METHOD_B = 0
    METHOD_C = 1
