'''_5915.py

BearingStiffnessModel
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_STIFFNESS_MODEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BearingStiffnessModel')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingStiffnessModel',)


class BearingStiffnessModel(Enum):
    '''BearingStiffnessModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_STIFFNESS_MODEL
    __hash__ = None

    LINEAR_CONCEPT_BEARINGS = 0
    SYSTEM_DEFLECTION_RESULT = 1
    NONLINEAR_BEARING_MODEL = 2
    LOAD_CASE_SETTING = 3
