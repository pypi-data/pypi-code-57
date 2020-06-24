'''_1182.py

CalculationMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CALCULATION_METHODS = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits', 'CalculationMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('CalculationMethods',)


class CalculationMethods(Enum):
    '''CalculationMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CALCULATION_METHODS
    __hash__ = None

    SPECIFY_PRESSURE = 0
    SPECIFY_INTERFERENCE = 1
