'''_5548.py

ClutchHalfCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2015
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5427
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5564
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ClutchHalfCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundModalAnalysisAtAStiffness',)


class ClutchHalfCompoundModalAnalysisAtAStiffness(_5564.CouplingHalfCompoundModalAnalysisAtAStiffness):
    '''ClutchHalfCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5427.ClutchHalfModalAnalysisAtAStiffness]':
        '''List[ClutchHalfModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5427.ClutchHalfModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_5427.ClutchHalfModalAnalysisAtAStiffness]':
        '''List[ClutchHalfModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_5427.ClutchHalfModalAnalysisAtAStiffness))
        return value
