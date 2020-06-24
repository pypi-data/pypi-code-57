'''_3372.py

WormGearMeshCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1818
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4331
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3374
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'WormGearMeshCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundSingleMeshWhineAnalysis',)


class WormGearMeshCompoundSingleMeshWhineAnalysis(_3374.GearMeshCompoundSingleMeshWhineAnalysis):
    '''WormGearMeshCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4331.WormGearMeshSingleMeshWhineAnalysis]':
        '''List[WormGearMeshSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4331.WormGearMeshSingleMeshWhineAnalysis))
        return value

    @property
    def connection_single_mesh_whine_analysis_load_cases(self) -> 'List[_4331.WormGearMeshSingleMeshWhineAnalysis]':
        '''List[WormGearMeshSingleMeshWhineAnalysis]: 'ConnectionSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSingleMeshWhineAnalysisLoadCases, constructor.new(_4331.WormGearMeshSingleMeshWhineAnalysis))
        return value
