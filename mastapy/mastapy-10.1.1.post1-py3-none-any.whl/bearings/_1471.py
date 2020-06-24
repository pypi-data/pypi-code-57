'''_1471.py

DynamicCapacityCalculationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMIC_CAPACITY_CALCULATION_METHOD = python_net_import('SMT.MastaAPI.Bearings', 'DynamicCapacityCalculationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCapacityCalculationMethod',)


class DynamicCapacityCalculationMethod(Enum):
    '''DynamicCapacityCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _DYNAMIC_CAPACITY_CALCULATION_METHOD
    __hash__ = None

    ISO_2812007_STANDARD = 0
    ISO_281_A52011_HYBRID_BEARING_WITH_SILICON_NITRIDE_ELEMENTS = 1
    ISOTR_128112008E_USING_ACTUAL_BEARING_INTERNAL_GEOMETRY = 2
    USERSPECIFIED = 3
