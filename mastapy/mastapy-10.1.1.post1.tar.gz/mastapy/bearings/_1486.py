'''_1486.py

StaticCapacityCalculationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STATIC_CAPACITY_CALCULATION_METHOD = python_net_import('SMT.MastaAPI.Bearings', 'StaticCapacityCalculationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticCapacityCalculationMethod',)


class StaticCapacityCalculationMethod(Enum):
    '''StaticCapacityCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _STATIC_CAPACITY_CALCULATION_METHOD
    __hash__ = None

    ISO_76_STANDARD = 0
    ISO_76_SUPPLEMENT_2_HYBRID_BEARING_WITH_SILICON_NITRIDE_ELEMENTS = 1
    USERSPECIFIED = 2
