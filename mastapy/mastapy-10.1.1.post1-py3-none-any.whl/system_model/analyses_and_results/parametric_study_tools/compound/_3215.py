'''_3215.py

PointLoadCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4046
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3220
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PointLoadCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundParametricStudyTool',)


class PointLoadCompoundParametricStudyTool(_3220.VirtualComponentCompoundParametricStudyTool):
    '''PointLoadCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4046.PointLoadParametricStudyTool]':
        '''List[PointLoadParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4046.PointLoadParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4046.PointLoadParametricStudyTool]':
        '''List[PointLoadParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4046.PointLoadParametricStudyTool))
        return value
