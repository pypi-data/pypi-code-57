'''_3126.py

StraightBevelDiffGearMeshCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3896
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3127
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'StraightBevelDiffGearMeshCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshCompoundModalAnalysis',)


class StraightBevelDiffGearMeshCompoundModalAnalysis(_3127.BevelGearMeshCompoundModalAnalysis):
    '''StraightBevelDiffGearMeshCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3896.StraightBevelDiffGearMeshModalAnalysis]':
        '''List[StraightBevelDiffGearMeshModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3896.StraightBevelDiffGearMeshModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_3896.StraightBevelDiffGearMeshModalAnalysis]':
        '''List[StraightBevelDiffGearMeshModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_3896.StraightBevelDiffGearMeshModalAnalysis))
        return value
