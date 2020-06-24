'''_320.py

SafetyRequirementsAGMA
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SAFETY_REQUIREMENTS_AGMA = python_net_import('SMT.MastaAPI.Gears', 'SafetyRequirementsAGMA')


__docformat__ = 'restructuredtext en'
__all__ = ('SafetyRequirementsAGMA',)


class SafetyRequirementsAGMA(Enum):
    '''SafetyRequirementsAGMA

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SAFETY_REQUIREMENTS_AGMA
    __hash__ = None

    FEWER_THAN_1_FAILURE_IN_10_000 = 0
    FEWER_THAN_1_FAILURE_IN_1000 = 1
    FEWER_THAN_1_FAILURE_IN_100 = 2
    FEWER_THAN_1_FAILURE_IN_10 = 3
    FEWER_THAN_1_FAILURE_IN_2 = 4
