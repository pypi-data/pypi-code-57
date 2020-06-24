'''_3322.py

ZerolBevelGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3321, _3373, _3294
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4260
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ZerolBevelGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundSingleMeshWhineAnalysis',)


class ZerolBevelGearSetCompoundSingleMeshWhineAnalysis(_3294.BevelGearSetCompoundSingleMeshWhineAnalysis):
    '''ZerolBevelGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3321.ZerolBevelGearCompoundSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearCompoundSingleMeshWhineAnalysis]: 'ZerolBevelGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3321.ZerolBevelGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3373.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]: 'ZerolBevelMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3373.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4260.ZerolBevelGearSetSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4260.ZerolBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4260.ZerolBevelGearSetSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4260.ZerolBevelGearSetSingleMeshWhineAnalysis))
        return value
