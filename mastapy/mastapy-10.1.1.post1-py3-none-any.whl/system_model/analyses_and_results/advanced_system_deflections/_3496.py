'''_3496.py

StraightBevelGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1964
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2363
from mastapy.gears.rating.straight_bevel import _403
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3495, _3433, _3474
from mastapy.system_model.analyses_and_results.system_deflections import _2362
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'StraightBevelGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetAdvancedSystemDeflection',)


class StraightBevelGearSetAdvancedSystemDeflection(_3474.BevelGearSetAdvancedSystemDeflection):
    '''StraightBevelGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1964.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1964.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2363.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2363.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_403.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_403.StraightBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_403.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_403.StraightBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def straight_bevel_gears_advanced_system_deflection(self) -> 'List[_3495.StraightBevelGearAdvancedSystemDeflection]':
        '''List[StraightBevelGearAdvancedSystemDeflection]: 'StraightBevelGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsAdvancedSystemDeflection, constructor.new(_3495.StraightBevelGearAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_meshes_advanced_system_deflection(self) -> 'List[_3433.StraightBevelGearMeshAdvancedSystemDeflection]':
        '''List[StraightBevelGearMeshAdvancedSystemDeflection]: 'StraightBevelMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesAdvancedSystemDeflection, constructor.new(_3433.StraightBevelGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2362.StraightBevelGearSetSystemDeflection]':
        '''List[StraightBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2362.StraightBevelGearSetSystemDeflection))
        return value
