'''_5969.py

InertiaAdjustedLoadCasePeriodMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_INERTIA_ADJUSTED_LOAD_CASE_PERIOD_METHOD = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'InertiaAdjustedLoadCasePeriodMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('InertiaAdjustedLoadCasePeriodMethod',)


class InertiaAdjustedLoadCasePeriodMethod(Enum):
    '''InertiaAdjustedLoadCasePeriodMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _INERTIA_ADJUSTED_LOAD_CASE_PERIOD_METHOD
    __hash__ = None

    TIME_PERIOD = 0
    POWER_LOAD_ANGLE = 1
