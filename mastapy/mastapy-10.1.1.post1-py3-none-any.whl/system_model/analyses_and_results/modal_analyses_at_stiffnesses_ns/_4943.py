'''_4943.py

ClutchConnectionModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.couplings import _1822
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2225
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4959
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ClutchConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionModalAnalysesAtStiffnesses',)


class ClutchConnectionModalAnalysesAtStiffnesses(_4959.CouplingConnectionModalAnalysesAtStiffnesses):
    '''ClutchConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionModalAnalysesAtStiffnesses.TYPE'):
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
