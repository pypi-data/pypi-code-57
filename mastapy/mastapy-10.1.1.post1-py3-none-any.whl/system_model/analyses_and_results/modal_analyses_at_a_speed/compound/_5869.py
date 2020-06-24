'''_5869.py

SynchroniserSleeveCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2025
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5751
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5868
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'SynchroniserSleeveCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundModalAnalysisAtASpeed',)


class SynchroniserSleeveCompoundModalAnalysisAtASpeed(_5868.SynchroniserPartCompoundModalAnalysisAtASpeed):
    '''SynchroniserSleeveCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5751.SynchroniserSleeveModalAnalysisAtASpeed]':
        '''List[SynchroniserSleeveModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5751.SynchroniserSleeveModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5751.SynchroniserSleeveModalAnalysisAtASpeed]':
        '''List[SynchroniserSleeveModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_5751.SynchroniserSleeveModalAnalysisAtASpeed))
        return value
