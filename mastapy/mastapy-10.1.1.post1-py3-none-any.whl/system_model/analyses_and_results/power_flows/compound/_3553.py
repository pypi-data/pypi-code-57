'''_3553.py

StraightBevelGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3552, _3608, _3531
from mastapy.system_model.analyses_and_results.power_flows import _4204
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundPowerFlow',)


class StraightBevelGearSetCompoundPowerFlow(_3531.BevelGearSetCompoundPowerFlow):
    '''StraightBevelGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2007.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_power_flow(self) -> 'List[_3552.StraightBevelGearCompoundPowerFlow]':
        '''List[StraightBevelGearCompoundPowerFlow]: 'StraightBevelGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundPowerFlow, constructor.new(_3552.StraightBevelGearCompoundPowerFlow))
        return value

    @property
    def straight_bevel_meshes_compound_power_flow(self) -> 'List[_3608.StraightBevelGearMeshCompoundPowerFlow]':
        '''List[StraightBevelGearMeshCompoundPowerFlow]: 'StraightBevelMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundPowerFlow, constructor.new(_3608.StraightBevelGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4204.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4204.StraightBevelGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_4204.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_4204.StraightBevelGearSetPowerFlow))
        return value
