'''_504.py

TipReliefScuffingOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TIP_RELIEF_SCUFFING_OPTIONS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'TipReliefScuffingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TipReliefScuffingOptions',)


class TipReliefScuffingOptions(Enum):
    '''TipReliefScuffingOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TIP_RELIEF_SCUFFING_OPTIONS
    __hash__ = None

    CALCULATE_USING_MICRO_GEOMETRY = 0
    CALCULATE_USING_MICRO_GEOMETRY_LIMIT_TO_OPTIMAL = 1
