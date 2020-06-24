'''_5838.py

PlanetaryConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1776
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5720
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5850
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'PlanetaryConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundModalAnalysisAtASpeed',)


class PlanetaryConnectionCompoundModalAnalysisAtASpeed(_5850.ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    '''PlanetaryConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1776.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1776.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1776.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1776.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5720.PlanetaryConnectionModalAnalysisAtASpeed]':
        '''List[PlanetaryConnectionModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5720.PlanetaryConnectionModalAnalysisAtASpeed))
        return value

    @property
    def connection_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5720.PlanetaryConnectionModalAnalysisAtASpeed]':
        '''List[PlanetaryConnectionModalAnalysisAtASpeed]: 'ConnectionModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtASpeedLoadCases, constructor.new(_5720.PlanetaryConnectionModalAnalysisAtASpeed))
        return value
