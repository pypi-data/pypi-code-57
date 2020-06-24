'''_5186.py

ClutchConnectionModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets.couplings import _1822
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2225
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5202
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ClutchConnectionModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionModalAnalysesAtSpeeds',)


class ClutchConnectionModalAnalysesAtSpeeds(_5202.CouplingConnectionModalAnalysesAtSpeeds):
    '''ClutchConnectionModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1822.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1822.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2225.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
