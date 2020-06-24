'''_5030.py

InertiaAdjustedLoadCaseResultsToCreate
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_INERTIA_ADJUSTED_LOAD_CASE_RESULTS_TO_CREATE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'InertiaAdjustedLoadCaseResultsToCreate')


__docformat__ = 'restructuredtext en'
__all__ = ('InertiaAdjustedLoadCaseResultsToCreate',)


class InertiaAdjustedLoadCaseResultsToCreate(Enum):
    '''InertiaAdjustedLoadCaseResultsToCreate

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _INERTIA_ADJUSTED_LOAD_CASE_RESULTS_TO_CREATE

    __hash__ = None

    LOAD_CASES_OVER_TIME = 0
    PEAK_LOADS_FOR_GEARS = 1
    ALL = 2
