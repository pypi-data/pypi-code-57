'''_6143.py

StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _6015
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6063
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis',)


class StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis(_6063.BevelGearMeshCompoundMultiBodyDynamicsAnalysis):
    '''StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6015.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6015.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis))
        return value

    @property
    def connection_multi_body_dynamics_analysis_load_cases(self) -> 'List[_6015.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]: 'ConnectionMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultiBodyDynamicsAnalysisLoadCases, constructor.new(_6015.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis))
        return value
