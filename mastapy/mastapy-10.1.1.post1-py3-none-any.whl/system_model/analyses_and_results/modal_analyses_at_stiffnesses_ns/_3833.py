'''_3833.py

TorqueConverterConnectionModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.couplings import _1904
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3756
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'TorqueConverterConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionModalAnalysesAtStiffnesses',)


class TorqueConverterConnectionModalAnalysesAtStiffnesses(_3756.CouplingConnectionModalAnalysesAtStiffnesses):
    '''TorqueConverterConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1904.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6199.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6199.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
