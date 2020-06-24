'''_4595.py

BoltCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4474
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4601
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BoltCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundModalAnalysisAtASpeed',)


class BoltCompoundModalAnalysisAtASpeed(_4601.ComponentCompoundModalAnalysisAtASpeed):
    '''BoltCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4474.BoltModalAnalysisAtASpeed]':
        '''List[BoltModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4474.BoltModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4474.BoltModalAnalysisAtASpeed]':
        '''List[BoltModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4474.BoltModalAnalysisAtASpeed))
        return value
