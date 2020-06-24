'''_3711.py

ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1824
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4242
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3712
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis',)


class ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis(_3712.CouplingConnectionCompoundSingleMeshWhineAnalysis):
    '''ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1824.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1824.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1824.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1824.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4242.ConceptCouplingConnectionSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingConnectionSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4242.ConceptCouplingConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def connection_single_mesh_whine_analysis_load_cases(self) -> 'List[_4242.ConceptCouplingConnectionSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingConnectionSingleMeshWhineAnalysis]: 'ConnectionSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSingleMeshWhineAnalysisLoadCases, constructor.new(_4242.ConceptCouplingConnectionSingleMeshWhineAnalysis))
        return value
