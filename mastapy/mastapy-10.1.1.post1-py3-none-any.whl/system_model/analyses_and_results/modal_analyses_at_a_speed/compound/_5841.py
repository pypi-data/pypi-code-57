'''_5841.py

PointLoadCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5723
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5875
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'PointLoadCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundModalAnalysisAtASpeed',)


class PointLoadCompoundModalAnalysisAtASpeed(_5875.VirtualComponentCompoundModalAnalysisAtASpeed):
    '''PointLoadCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5723.PointLoadModalAnalysisAtASpeed]':
        '''List[PointLoadModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5723.PointLoadModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5723.PointLoadModalAnalysisAtASpeed]':
        '''List[PointLoadModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_5723.PointLoadModalAnalysisAtASpeed))
        return value
