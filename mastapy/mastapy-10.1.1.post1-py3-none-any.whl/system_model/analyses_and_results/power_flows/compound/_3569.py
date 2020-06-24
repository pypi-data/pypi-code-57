'''_3569.py

PulleyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2041
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4102
from mastapy.system_model.analyses_and_results.power_flows.compound import _3566
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PulleyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundPowerFlow',)


class PulleyCompoundPowerFlow(_3566.CouplingHalfCompoundPowerFlow):
    '''PulleyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2041.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2041.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4102.PulleyPowerFlow]':
        '''List[PulleyPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4102.PulleyPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4102.PulleyPowerFlow]':
        '''List[PulleyPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4102.PulleyPowerFlow))
        return value
