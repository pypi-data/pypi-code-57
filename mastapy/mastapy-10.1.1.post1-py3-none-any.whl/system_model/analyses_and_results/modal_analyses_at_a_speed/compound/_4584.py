'''_4584.py

BearingCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4462
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4612
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BearingCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundModalAnalysisAtASpeed',)


class BearingCompoundModalAnalysisAtASpeed(_4612.ConnectorCompoundModalAnalysisAtASpeed):
    '''BearingCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4462.BearingModalAnalysisAtASpeed]':
        '''List[BearingModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4462.BearingModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4462.BearingModalAnalysisAtASpeed]':
        '''List[BearingModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4462.BearingModalAnalysisAtASpeed))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundModalAnalysisAtASpeed]':
        '''List[BearingCompoundModalAnalysisAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundModalAnalysisAtASpeed))
        return value
