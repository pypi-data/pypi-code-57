'''_3492.py

SpiralBevelGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1966
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2355
from mastapy.gears.rating.spiral_bevel import _404
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3491, _3432, _3474
from mastapy.system_model.analyses_and_results.system_deflections import _2354
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'SpiralBevelGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetAdvancedSystemDeflection',)


class SpiralBevelGearSetAdvancedSystemDeflection(_3474.BevelGearSetAdvancedSystemDeflection):
    '''SpiralBevelGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2355.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2355.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_404.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_404.SpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_404.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_404.SpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def spiral_bevel_gears_advanced_system_deflection(self) -> 'List[_3491.SpiralBevelGearAdvancedSystemDeflection]':
        '''List[SpiralBevelGearAdvancedSystemDeflection]: 'SpiralBevelGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsAdvancedSystemDeflection, constructor.new(_3491.SpiralBevelGearAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_meshes_advanced_system_deflection(self) -> 'List[_3432.SpiralBevelGearMeshAdvancedSystemDeflection]':
        '''List[SpiralBevelGearMeshAdvancedSystemDeflection]: 'SpiralBevelMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesAdvancedSystemDeflection, constructor.new(_3432.SpiralBevelGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2354.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2354.SpiralBevelGearSetSystemDeflection))
        return value
