'''_3024.py

ZerolBevelGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2012
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.gears.rating.zerol_bevel import _386
from mastapy.system_model.analyses_and_results.system_deflections import _2233
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3114
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ZerolBevelGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearAdvancedSystemDeflection',)


class ZerolBevelGearAdvancedSystemDeflection(_3114.BevelGearAdvancedSystemDeflection):
    '''ZerolBevelGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2234.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_386.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_386.ZerolBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2233.ZerolBevelGearSystemDeflection]':
        '''List[ZerolBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2233.ZerolBevelGearSystemDeflection))
        return value
