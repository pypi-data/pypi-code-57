'''_1718.py

StressConcentrationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STRESS_CONCENTRATION_METHOD = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'StressConcentrationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('StressConcentrationMethod',)


class StressConcentrationMethod(Enum):
    '''StressConcentrationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _STRESS_CONCENTRATION_METHOD

    __hash__ = None

    BASIC_STRESS_RISER_FUNCTION = 0
    CALCULATED_STRESSES = 1
