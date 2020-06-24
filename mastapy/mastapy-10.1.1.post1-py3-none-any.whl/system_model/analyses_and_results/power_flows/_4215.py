'''_4215.py

CylindricalGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2328
from mastapy.gears.rating.cylindrical import _397
from mastapy.system_model.analyses_and_results.power_flows import _4214, _4164, _4218
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CylindricalGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetPowerFlow',)


class CylindricalGearSetPowerFlow(_4218.GearSetPowerFlow):
    '''CylindricalGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2328.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2328.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_397.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_397.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_397.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_397.CylindricalGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def cylindrical_gears_power_flow(self) -> 'List[_4214.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'CylindricalGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsPowerFlow, constructor.new(_4214.CylindricalGearPowerFlow))
        return value

    @property
    def cylindrical_meshes_power_flow(self) -> 'List[_4164.CylindricalGearMeshPowerFlow]':
        '''List[CylindricalGearMeshPowerFlow]: 'CylindricalMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesPowerFlow, constructor.new(_4164.CylindricalGearMeshPowerFlow))
        return value

    @property
    def ratings_for_all_designs(self) -> 'List[_397.CylindricalGearSetRating]':
        '''List[CylindricalGearSetRating]: 'RatingsForAllDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RatingsForAllDesigns, constructor.new(_397.CylindricalGearSetRating))
        return value
