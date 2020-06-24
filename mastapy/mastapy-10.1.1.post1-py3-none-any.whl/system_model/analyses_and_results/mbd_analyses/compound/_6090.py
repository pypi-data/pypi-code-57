'''_6090.py

CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5950
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6100
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis',)


class CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis(_6100.GearMeshCompoundMultiBodyDynamicsAnalysis):
    '''CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5950.CylindricalGearMeshMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5950.CylindricalGearMeshMultiBodyDynamicsAnalysis))
        return value

    @property
    def connection_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5950.CylindricalGearMeshMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultiBodyDynamicsAnalysis]: 'ConnectionMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5950.CylindricalGearMeshMultiBodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value
