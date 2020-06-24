'''_5603.py

ShaftCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5494
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5528
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ShaftCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundModalAnalysisAtAStiffness',)


class ShaftCompoundModalAnalysisAtAStiffness(_5528.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness):
    '''ShaftCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5494.ShaftModalAnalysisAtAStiffness]':
        '''List[ShaftModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5494.ShaftModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_5494.ShaftModalAnalysisAtAStiffness]':
        '''List[ShaftModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_5494.ShaftModalAnalysisAtAStiffness))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundModalAnalysisAtAStiffness))
        return value
