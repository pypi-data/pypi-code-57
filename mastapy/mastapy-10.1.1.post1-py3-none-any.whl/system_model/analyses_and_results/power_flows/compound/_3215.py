'''_3215.py

ShaftHubConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1967
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4132
from mastapy.system_model.analyses_and_results.power_flows.compound import _3146
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ShaftHubConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundPowerFlow',)


class ShaftHubConnectionCompoundPowerFlow(_3146.ConnectorCompoundPowerFlow):
    '''ShaftHubConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4132.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4132.ShaftHubConnectionPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4132.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4132.ShaftHubConnectionPowerFlow))
        return value
