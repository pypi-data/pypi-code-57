'''_3534.py

CylindricalGearCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.cylindrical import _472
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _1984
from mastapy.system_model.analyses_and_results.power_flows import _4185
from mastapy.system_model.analyses_and_results.power_flows.compound import _3537
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CylindricalGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundPowerFlow',)


class CylindricalGearCompoundPowerFlow(_3537.GearCompoundPowerFlow):
    '''CylindricalGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_duty_cycle_rating(self) -> '_472.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_472.CylindricalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def cylindrical_gear_duty_cycle_rating(self) -> '_472.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'CylindricalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_472.CylindricalGearDutyCycleRating)(self.wrapped.CylindricalGearDutyCycleRating) if self.wrapped.CylindricalGearDutyCycleRating else None

    @property
    def component_design(self) -> '_1984.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4185.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4185.CylindricalGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4185.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4185.CylindricalGearPowerFlow))
        return value
