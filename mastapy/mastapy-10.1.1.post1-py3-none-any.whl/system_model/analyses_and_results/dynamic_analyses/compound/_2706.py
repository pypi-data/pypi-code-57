'''_2706.py

KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2705, _2767, _2704
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3723
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis(_2704.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_dynamic_analysis(self) -> 'List[_2705.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundDynamicAnalysis, constructor.new(_2705.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_dynamic_analysis(self) -> 'List[_2767.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundDynamicAnalysis, constructor.new(_2767.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis))
        return value
