'''_4911.py

ParametricStudyDimension
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_DIMENSION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyDimension',)


class ParametricStudyDimension(Enum):
    '''ParametricStudyDimension

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PARAMETRIC_STUDY_DIMENSION
    __hash__ = None

    DIMENSION_1 = 1
    DIMENSION_2 = 2
