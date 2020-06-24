'''_6359.py

ZerolBevelGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2093
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.gears.rating.zerol_bevel import _173
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6357, _6358, _6251
from mastapy.system_model.analyses_and_results.system_deflections import _2344
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ZerolBevelGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetAdvancedSystemDeflection',)


class ZerolBevelGearSetAdvancedSystemDeflection(_6251.BevelGearSetAdvancedSystemDeflection):
    '''ZerolBevelGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6214.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_173.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_173.ZerolBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_173.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_173.ZerolBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def zerol_bevel_gears_advanced_system_deflection(self) -> 'List[_6357.ZerolBevelGearAdvancedSystemDeflection]':
        '''List[ZerolBevelGearAdvancedSystemDeflection]: 'ZerolBevelGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsAdvancedSystemDeflection, constructor.new(_6357.ZerolBevelGearAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_meshes_advanced_system_deflection(self) -> 'List[_6358.ZerolBevelGearMeshAdvancedSystemDeflection]':
        '''List[ZerolBevelGearMeshAdvancedSystemDeflection]: 'ZerolBevelMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesAdvancedSystemDeflection, constructor.new(_6358.ZerolBevelGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2344.ZerolBevelGearSetSystemDeflection]':
        '''List[ZerolBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2344.ZerolBevelGearSetSystemDeflection))
        return value
