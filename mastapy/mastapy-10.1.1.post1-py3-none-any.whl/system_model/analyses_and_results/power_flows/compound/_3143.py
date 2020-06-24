'''_3143.py

BoltCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4177
from mastapy.system_model.analyses_and_results.power_flows.compound import _3145
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BoltCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundPowerFlow',)


class BoltCompoundPowerFlow(_3145.ComponentCompoundPowerFlow):
    '''BoltCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4177.BoltPowerFlow]':
        '''List[BoltPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4177.BoltPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4177.BoltPowerFlow]':
        '''List[BoltPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4177.BoltPowerFlow))
        return value
