'''_5035.py

TorqueConverterConnectionModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.couplings import _1830
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2232
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4959
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'TorqueConverterConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionModalAnalysesAtStiffnesses',)


class TorqueConverterConnectionModalAnalysesAtStiffnesses(_4959.CouplingConnectionModalAnalysesAtStiffnesses):
    '''TorqueConverterConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2232.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2232.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
