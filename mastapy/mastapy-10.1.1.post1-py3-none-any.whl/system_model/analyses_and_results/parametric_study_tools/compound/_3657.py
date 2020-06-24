'''_3657.py

HypoidGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2074
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3655, _3656, _3604
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3526
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'HypoidGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundParametricStudyTool',)


class HypoidGearSetCompoundParametricStudyTool(_3604.AGMAGleasonConicalGearSetCompoundParametricStudyTool):
    '''HypoidGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2074.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2074.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_parametric_study_tool(self) -> 'List[_3655.HypoidGearCompoundParametricStudyTool]':
        '''List[HypoidGearCompoundParametricStudyTool]: 'HypoidGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundParametricStudyTool, constructor.new(_3655.HypoidGearCompoundParametricStudyTool))
        return value

    @property
    def hypoid_meshes_compound_parametric_study_tool(self) -> 'List[_3656.HypoidGearMeshCompoundParametricStudyTool]':
        '''List[HypoidGearMeshCompoundParametricStudyTool]: 'HypoidMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundParametricStudyTool, constructor.new(_3656.HypoidGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3526.HypoidGearSetParametricStudyTool]':
        '''List[HypoidGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3526.HypoidGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3526.HypoidGearSetParametricStudyTool]':
        '''List[HypoidGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3526.HypoidGearSetParametricStudyTool))
        return value
