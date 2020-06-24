'''_576.py

LocationOfTipReliefEvaluation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LOCATION_OF_TIP_RELIEF_EVALUATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'LocationOfTipReliefEvaluation')


__docformat__ = 'restructuredtext en'
__all__ = ('LocationOfTipReliefEvaluation',)


class LocationOfTipReliefEvaluation(Enum):
    '''LocationOfTipReliefEvaluation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LOCATION_OF_TIP_RELIEF_EVALUATION
    __hash__ = None

    TIP_FORM = 0
    UPPER_EVALUATION_LIMIT = 1
    USERSPECIFIED = 2
