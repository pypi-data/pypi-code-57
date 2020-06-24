'''_2827.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1993
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2826, _2887, _2823
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3843
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis(_2823.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1993.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1993.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_gear_whine_analysis(self) -> 'List[_2826.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundGearWhineAnalysis, constructor.new(_2826.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_gear_whine_analysis(self) -> 'List[_2887.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundGearWhineAnalysis, constructor.new(_2887.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3843.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3843.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_3843.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_3843.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis))
        return value
