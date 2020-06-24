'''_3488.py

KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2348
from mastapy.gears.rating.klingelnberg_spiral_bevel import _418
from mastapy.system_model.analyses_and_results.system_deflections import _2347
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3484
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection(_3484.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_418.KlingelnbergCycloPalloidSpiralBevelGearRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_418.KlingelnbergCycloPalloidSpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection))
        return value
