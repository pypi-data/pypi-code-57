'''_4869.py

ConceptCouplingCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4725
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4880
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConceptCouplingCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundModalAnalysis',)


class ConceptCouplingCompoundModalAnalysis(_4880.CouplingCompoundModalAnalysis):
    '''ConceptCouplingCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4725.ConceptCouplingModalAnalysis]':
        '''List[ConceptCouplingModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4725.ConceptCouplingModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4725.ConceptCouplingModalAnalysis]':
        '''List[ConceptCouplingModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4725.ConceptCouplingModalAnalysis))
        return value
