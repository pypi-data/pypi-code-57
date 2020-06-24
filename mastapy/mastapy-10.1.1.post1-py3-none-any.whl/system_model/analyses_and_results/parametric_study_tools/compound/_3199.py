'''_3199.py

BoltCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4030
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3201
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BoltCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundParametricStudyTool',)


class BoltCompoundParametricStudyTool(_3201.ComponentCompoundParametricStudyTool):
    '''BoltCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4030.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4030.BoltParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4030.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4030.BoltParametricStudyTool))
        return value
