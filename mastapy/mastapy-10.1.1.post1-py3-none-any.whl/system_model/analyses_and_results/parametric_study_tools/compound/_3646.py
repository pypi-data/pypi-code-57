'''_3646.py

ExternalCADModelCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3515
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3623
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ExternalCADModelCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundParametricStudyTool',)


class ExternalCADModelCompoundParametricStudyTool(_3623.ComponentCompoundParametricStudyTool):
    '''ExternalCADModelCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3515.ExternalCADModelParametricStudyTool]':
        '''List[ExternalCADModelParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3515.ExternalCADModelParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3515.ExternalCADModelParametricStudyTool]':
        '''List[ExternalCADModelParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3515.ExternalCADModelParametricStudyTool))
        return value
