'''_6290.py

AdditionalForcesObtainedFrom
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ADDITIONAL_FORCES_OBTAINED_FROM = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'AdditionalForcesObtainedFrom')


__docformat__ = 'restructuredtext en'
__all__ = ('AdditionalForcesObtainedFrom',)


class AdditionalForcesObtainedFrom(Enum):
    '''AdditionalForcesObtainedFrom

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ADDITIONAL_FORCES_OBTAINED_FROM
    __hash__ = None

    LARGEST_MAGNITUDE = 0
    MEDIAN_VALUE = 1
    AVERAGE_VALUE = 2
