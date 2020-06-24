'''_4971.py

AnalysisTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ANALYSIS_TYPES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'AnalysisTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('AnalysisTypes',)


class AnalysisTypes(Enum):
    '''AnalysisTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _ANALYSIS_TYPES

    __hash__ = None

    NORMAL = 0
    RUN_UP = 1
    SIMULINK = 2
    DRIVE_CYCLE = 3
    DRIVE_CYCLE_WITH_SIMULINK = 4
