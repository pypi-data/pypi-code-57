'''_3666.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2000
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3665, _3726, _3662
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4315
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis(_3662.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2000.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2000.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3665.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3665.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3726.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3726.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4315.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4315.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4315.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4315.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis))
        return value
