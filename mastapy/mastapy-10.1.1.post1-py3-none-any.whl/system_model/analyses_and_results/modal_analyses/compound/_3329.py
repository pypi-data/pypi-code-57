'''_3329.py

ConceptCouplingHalfCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2040
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3861
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3331
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConceptCouplingHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundModalAnalysis',)


class ConceptCouplingHalfCompoundModalAnalysis(_3331.CouplingHalfCompoundModalAnalysis):
    '''ConceptCouplingHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2040.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2040.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3861.ConceptCouplingHalfModalAnalysis]':
        '''List[ConceptCouplingHalfModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3861.ConceptCouplingHalfModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3861.ConceptCouplingHalfModalAnalysis]':
        '''List[ConceptCouplingHalfModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3861.ConceptCouplingHalfModalAnalysis))
        return value
