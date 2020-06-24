'''_3163.py

TorqueConverterCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2037
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3994
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3149
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'TorqueConverterCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundParametricStudyTool',)


class TorqueConverterCompoundParametricStudyTool(_3149.CouplingCompoundParametricStudyTool):
    '''TorqueConverterCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2037.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2037.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2037.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2037.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3994.TorqueConverterParametricStudyTool]':
        '''List[TorqueConverterParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3994.TorqueConverterParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3994.TorqueConverterParametricStudyTool]':
        '''List[TorqueConverterParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3994.TorqueConverterParametricStudyTool))
        return value
