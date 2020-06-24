'''_3307.py

KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3306, _3368, _3305
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4384
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis(_3305.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_single_mesh_whine_analysis(self) -> 'List[_3306.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundSingleMeshWhineAnalysis, constructor.new(_3306.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_3368.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_3368.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4384.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4384.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_4384.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_4384.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis))
        return value
