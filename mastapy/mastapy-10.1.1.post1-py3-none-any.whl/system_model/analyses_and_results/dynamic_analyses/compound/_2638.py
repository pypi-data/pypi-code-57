'''_2638.py

HypoidGearMeshCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1804
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3664
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2636
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'HypoidGearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCompoundDynamicAnalysis',)


class HypoidGearMeshCompoundDynamicAnalysis(_2636.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis):
    '''HypoidGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3664.HypoidGearMeshDynamicAnalysis]':
        '''List[HypoidGearMeshDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3664.HypoidGearMeshDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_3664.HypoidGearMeshDynamicAnalysis]':
        '''List[HypoidGearMeshDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_3664.HypoidGearMeshDynamicAnalysis))
        return value
