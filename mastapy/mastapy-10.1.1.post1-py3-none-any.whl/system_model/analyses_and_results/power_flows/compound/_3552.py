'''_3552.py

StraightBevelGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4203
from mastapy.system_model.analyses_and_results.power_flows.compound import _3530
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundPowerFlow',)


class StraightBevelGearCompoundPowerFlow(_3530.BevelGearCompoundPowerFlow):
    '''StraightBevelGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4203.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4203.StraightBevelGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4203.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4203.StraightBevelGearPowerFlow))
        return value
