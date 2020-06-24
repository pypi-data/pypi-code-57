'''_4219.py

BeltConnectionModalAnalysisAtAStiffness
'''


from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6055
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4272
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BeltConnectionModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionModalAnalysisAtAStiffness',)


class BeltConnectionModalAnalysisAtAStiffness(_4272.InterMountableComponentConnectionModalAnalysisAtAStiffness):
    '''BeltConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6055.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6055.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
