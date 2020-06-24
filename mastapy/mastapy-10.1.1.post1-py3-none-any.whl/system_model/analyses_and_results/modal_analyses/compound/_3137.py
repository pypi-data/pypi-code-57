'''_3137.py

WormGearMeshCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1818
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3907
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3139
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'WormGearMeshCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundModalAnalysis',)


class WormGearMeshCompoundModalAnalysis(_3139.GearMeshCompoundModalAnalysis):
    '''WormGearMeshCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3907.WormGearMeshModalAnalysis]':
        '''List[WormGearMeshModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3907.WormGearMeshModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_3907.WormGearMeshModalAnalysis]':
        '''List[WormGearMeshModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_3907.WormGearMeshModalAnalysis))
        return value
