'''_3360.py

BevelDifferentialGearMeshCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1790
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3892
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3364
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BevelDifferentialGearMeshCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshCompoundModalAnalysis',)


class BevelDifferentialGearMeshCompoundModalAnalysis(_3364.BevelGearMeshCompoundModalAnalysis):
    '''BevelDifferentialGearMeshCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3892.BevelDifferentialGearMeshModalAnalysis]':
        '''List[BevelDifferentialGearMeshModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3892.BevelDifferentialGearMeshModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_3892.BevelDifferentialGearMeshModalAnalysis]':
        '''List[BevelDifferentialGearMeshModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_3892.BevelDifferentialGearMeshModalAnalysis))
        return value
