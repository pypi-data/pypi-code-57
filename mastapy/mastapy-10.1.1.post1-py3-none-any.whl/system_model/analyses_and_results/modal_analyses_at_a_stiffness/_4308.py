'''_4308.py

SpringDamperConnectionModalAnalysisAtAStiffness
'''


from mastapy.system_model.connections_and_sockets.couplings import _1902
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6181
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4247
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SpringDamperConnectionModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionModalAnalysisAtAStiffness',)


class SpringDamperConnectionModalAnalysisAtAStiffness(_4247.CouplingConnectionModalAnalysisAtAStiffness):
    '''SpringDamperConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1902.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1902.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6181.SpringDamperConnectionLoadCase':
        '''SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6181.SpringDamperConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
