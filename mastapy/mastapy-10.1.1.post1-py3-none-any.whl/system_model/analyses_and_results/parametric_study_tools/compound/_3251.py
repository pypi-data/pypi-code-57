'''_3251.py

SpiralBevelGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3250, _3191, _3233
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4082
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'SpiralBevelGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundParametricStudyTool',)


class SpiralBevelGearSetCompoundParametricStudyTool(_3233.BevelGearSetCompoundParametricStudyTool):
    '''SpiralBevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2003.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2003.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_parametric_study_tool(self) -> 'List[_3250.SpiralBevelGearCompoundParametricStudyTool]':
        '''List[SpiralBevelGearCompoundParametricStudyTool]: 'SpiralBevelGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundParametricStudyTool, constructor.new(_3250.SpiralBevelGearCompoundParametricStudyTool))
        return value

    @property
    def spiral_bevel_meshes_compound_parametric_study_tool(self) -> 'List[_3191.SpiralBevelGearMeshCompoundParametricStudyTool]':
        '''List[SpiralBevelGearMeshCompoundParametricStudyTool]: 'SpiralBevelMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundParametricStudyTool, constructor.new(_3191.SpiralBevelGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4082.SpiralBevelGearSetParametricStudyTool]':
        '''List[SpiralBevelGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4082.SpiralBevelGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4082.SpiralBevelGearSetParametricStudyTool]':
        '''List[SpiralBevelGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4082.SpiralBevelGearSetParametricStudyTool))
        return value
