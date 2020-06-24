'''_1226.py

ComplexMagnitudeMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COMPLEX_MAGNITUDE_METHOD = python_net_import('SMT.MastaAPI.MathUtility', 'ComplexMagnitudeMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ComplexMagnitudeMethod',)


class ComplexMagnitudeMethod(Enum):
    '''ComplexMagnitudeMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _COMPLEX_MAGNITUDE_METHOD
    __hash__ = None

    MAXIMUM_MAGNITUDE_OVER_PERIOD = 0
    MAGNITUDE_OF_COMPLEX_MODULI = 1
    MAGNITUDE_OF_COMPLEX_VALUES = 2
