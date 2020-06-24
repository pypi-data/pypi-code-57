'''_5179.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2080
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5177, _5178, _5173
from mastapy.system_model.analyses_and_results.mbd_analyses import _5042
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis(_5173.KlingelnbergCycloPalloidConicalGearSetCompoundMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2080.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2080.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5177.KlingelnbergCycloPalloidSpiralBevelGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5177.KlingelnbergCycloPalloidSpiralBevelGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5178.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5178.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5042.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5042.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5042.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5042.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value
