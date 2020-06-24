'''_4201.py

TorqueConverterConnectionCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4079
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4127
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'TorqueConverterConnectionCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundModalAnalysesAtSpeeds',)


class TorqueConverterConnectionCompoundModalAnalysesAtSpeeds(_4127.CouplingConnectionCompoundModalAnalysesAtSpeeds):
    '''TorqueConverterConnectionCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1904.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1904.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4079.TorqueConverterConnectionModalAnalysesAtSpeeds]':
        '''List[TorqueConverterConnectionModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4079.TorqueConverterConnectionModalAnalysesAtSpeeds))
        return value

    @property
    def connection_modal_analyses_at_speeds_load_cases(self) -> 'List[_4079.TorqueConverterConnectionModalAnalysesAtSpeeds]':
        '''List[TorqueConverterConnectionModalAnalysesAtSpeeds]: 'ConnectionModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtSpeedsLoadCases, constructor.new(_4079.TorqueConverterConnectionModalAnalysesAtSpeeds))
        return value
