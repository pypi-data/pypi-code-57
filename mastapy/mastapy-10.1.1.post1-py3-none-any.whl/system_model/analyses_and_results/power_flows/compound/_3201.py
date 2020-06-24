'''_3201.py

WormGearCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.worm import _351
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _1998
from mastapy.system_model.analyses_and_results.power_flows import _4236
from mastapy.system_model.analyses_and_results.power_flows.compound import _3182
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'WormGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundPowerFlow',)


class WormGearCompoundPowerFlow(_3182.GearCompoundPowerFlow):
    '''WormGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_duty_cycle_rating(self) -> '_351.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_351.WormGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def worm_gear_duty_cycle_rating(self) -> '_351.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'WormGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_351.WormGearDutyCycleRating)(self.wrapped.WormGearDutyCycleRating) if self.wrapped.WormGearDutyCycleRating else None

    @property
    def component_design(self) -> '_1998.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4236.WormGearPowerFlow]':
        '''List[WormGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4236.WormGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4236.WormGearPowerFlow]':
        '''List[WormGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4236.WormGearPowerFlow))
        return value
