'''_6146.py

StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1816
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _6018
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6063
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis',)


class StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis(_6063.BevelGearMeshCompoundMultiBodyDynamicsAnalysis):
    '''StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6018.StraightBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6018.StraightBevelGearMeshMultiBodyDynamicsAnalysis))
        return value

    @property
    def connection_multi_body_dynamics_analysis_load_cases(self) -> 'List[_6018.StraightBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshMultiBodyDynamicsAnalysis]: 'ConnectionMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultiBodyDynamicsAnalysisLoadCases, constructor.new(_6018.StraightBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
