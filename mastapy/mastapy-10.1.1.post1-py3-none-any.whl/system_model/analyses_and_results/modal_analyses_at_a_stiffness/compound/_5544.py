'''_5544.py

BoltCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5425
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5550
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'BoltCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundModalAnalysisAtAStiffness',)


class BoltCompoundModalAnalysisAtAStiffness(_5550.ComponentCompoundModalAnalysisAtAStiffness):
    '''BoltCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5425.BoltModalAnalysisAtAStiffness]':
        '''List[BoltModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5425.BoltModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_5425.BoltModalAnalysisAtAStiffness]':
        '''List[BoltModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_5425.BoltModalAnalysisAtAStiffness))
        return value
