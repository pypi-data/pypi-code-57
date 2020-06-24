'''_4659.py

PowerLoadCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4538
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4692
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'PowerLoadCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundModalAnalysisAtASpeed',)


class PowerLoadCompoundModalAnalysisAtASpeed(_4692.VirtualComponentCompoundModalAnalysisAtASpeed):
    '''PowerLoadCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4538.PowerLoadModalAnalysisAtASpeed]':
        '''List[PowerLoadModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4538.PowerLoadModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4538.PowerLoadModalAnalysisAtASpeed]':
        '''List[PowerLoadModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4538.PowerLoadModalAnalysisAtASpeed))
        return value
