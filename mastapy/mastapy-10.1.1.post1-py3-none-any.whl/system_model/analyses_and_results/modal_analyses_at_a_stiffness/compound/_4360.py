'''_4360.py

ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1896
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4236
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4371
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness',)


class ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness(_4371.CouplingConnectionCompoundModalAnalysisAtAStiffness):
    '''ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1896.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1896.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1896.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1896.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4236.ConceptCouplingConnectionModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingConnectionModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4236.ConceptCouplingConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def connection_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4236.ConceptCouplingConnectionModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingConnectionModalAnalysisAtAStiffness]: 'ConnectionModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtAStiffnessLoadCases, constructor.new(_4236.ConceptCouplingConnectionModalAnalysisAtAStiffness))
        return value
