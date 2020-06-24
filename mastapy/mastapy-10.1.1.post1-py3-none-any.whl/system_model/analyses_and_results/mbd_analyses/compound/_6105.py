'''_6105.py

HypoidGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6103, _6104, _6052
from mastapy.system_model.analyses_and_results.mbd_analyses import _5967
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'HypoidGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundMultiBodyDynamicsAnalysis',)


class HypoidGearSetCompoundMultiBodyDynamicsAnalysis(_6052.AGMAGleasonConicalGearSetCompoundMultiBodyDynamicsAnalysis):
    '''HypoidGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_6103.HypoidGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearCompoundMultiBodyDynamicsAnalysis]: 'HypoidGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_6103.HypoidGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_6104.HypoidGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearMeshCompoundMultiBodyDynamicsAnalysis]: 'HypoidMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_6104.HypoidGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5967.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5967.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5967.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5967.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value
