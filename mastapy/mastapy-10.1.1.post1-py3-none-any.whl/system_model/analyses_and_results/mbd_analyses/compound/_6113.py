'''_6113.py

KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6111, _6112, _6110
from mastapy.system_model.analyses_and_results.mbd_analyses import _5979
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis(_6110.KlingelnbergCycloPalloidConicalGearSetCompoundMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_6111.KlingelnbergCycloPalloidHypoidGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_6111.KlingelnbergCycloPalloidHypoidGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_6112.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_6112.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5979.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5979.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5979.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5979.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis))
        return value
