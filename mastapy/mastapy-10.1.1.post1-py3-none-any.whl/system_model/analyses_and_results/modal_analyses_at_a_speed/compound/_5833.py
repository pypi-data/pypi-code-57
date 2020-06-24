'''_5833.py

MassDiscCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1926
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5714
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5875
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'MassDiscCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundModalAnalysisAtASpeed',)


class MassDiscCompoundModalAnalysisAtASpeed(_5875.VirtualComponentCompoundModalAnalysisAtASpeed):
    '''MassDiscCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5714.MassDiscModalAnalysisAtASpeed]':
        '''List[MassDiscModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5714.MassDiscModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5714.MassDiscModalAnalysisAtASpeed]':
        '''List[MassDiscModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_5714.MassDiscModalAnalysisAtASpeed))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundModalAnalysisAtASpeed]':
        '''List[MassDiscCompoundModalAnalysisAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundModalAnalysisAtASpeed))
        return value
