'''_3453.py

TorqueConverterPumpCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3331
from mastapy.system_model.analyses_and_results.power_flows.compound import _3379
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterPumpCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundPowerFlow',)


class TorqueConverterPumpCompoundPowerFlow(_3379.CouplingHalfCompoundPowerFlow):
    '''TorqueConverterPumpCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3331.TorqueConverterPumpPowerFlow]':
        '''List[TorqueConverterPumpPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3331.TorqueConverterPumpPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3331.TorqueConverterPumpPowerFlow]':
        '''List[TorqueConverterPumpPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3331.TorqueConverterPumpPowerFlow))
        return value
