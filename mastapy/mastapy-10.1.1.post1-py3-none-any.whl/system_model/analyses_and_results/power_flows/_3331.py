'''_3331.py

TorqueConverterPumpPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6201
from mastapy.system_model.analyses_and_results.power_flows import _3252
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'TorqueConverterPumpPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpPowerFlow',)


class TorqueConverterPumpPowerFlow(_3252.CouplingHalfPowerFlow):
    '''TorqueConverterPumpPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6201.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6201.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
