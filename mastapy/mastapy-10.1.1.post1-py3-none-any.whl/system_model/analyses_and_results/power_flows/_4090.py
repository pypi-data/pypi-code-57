'''_4090.py

WormGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _1982
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2166
from mastapy.gears.rating.worm import _353
from mastapy.system_model.analyses_and_results.power_flows import _4207, _4142, _4189
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'WormGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetPowerFlow',)


class WormGearSetPowerFlow(_4189.GearSetPowerFlow):
    '''WormGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1982.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2166.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_353.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_353.WormGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_353.WormGearSetRating':
        '''WormGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_353.WormGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def worm_gears_power_flow(self) -> 'List[_4207.WormGearPowerFlow]':
        '''List[WormGearPowerFlow]: 'WormGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsPowerFlow, constructor.new(_4207.WormGearPowerFlow))
        return value

    @property
    def worm_meshes_power_flow(self) -> 'List[_4142.WormGearMeshPowerFlow]':
        '''List[WormGearMeshPowerFlow]: 'WormMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesPowerFlow, constructor.new(_4142.WormGearMeshPowerFlow))
        return value
