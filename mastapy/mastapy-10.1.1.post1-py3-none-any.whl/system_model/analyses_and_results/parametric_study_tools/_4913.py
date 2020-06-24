'''_4913.py

ParametricStudyDOEResultVariableForParallelCoordinatesPlot
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_DOE_RESULT_VARIABLE_FOR_PARALLEL_COORDINATES_PLOT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyDOEResultVariableForParallelCoordinatesPlot')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyDOEResultVariableForParallelCoordinatesPlot',)


class ParametricStudyDOEResultVariableForParallelCoordinatesPlot(_1.APIBase):
    '''ParametricStudyDOEResultVariableForParallelCoordinatesPlot

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_DOE_RESULT_VARIABLE_FOR_PARALLEL_COORDINATES_PLOT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyDOEResultVariableForParallelCoordinatesPlot.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def move_up(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'MoveUp' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MoveUp

    @property
    def move_down(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'MoveDown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MoveDown

    @property
    def parameter_name(self) -> 'str':
        '''str: 'ParameterName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ParameterName

    @property
    def entity_name(self) -> 'str':
        '''str: 'EntityName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EntityName
