'''_3509.py

MeasurementComponentCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1927
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4159
from mastapy.system_model.analyses_and_results.power_flows.compound import _3518
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'MeasurementComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundPowerFlow',)


class MeasurementComponentCompoundPowerFlow(_3518.VirtualComponentCompoundPowerFlow):
    '''MeasurementComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4159.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4159.MeasurementComponentPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4159.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4159.MeasurementComponentPowerFlow))
        return value
