'''_3843.py

KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2350
from mastapy.system_model.analyses_and_results.system_deflections import _2349
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3842, _3785, _3839
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis(_3839.KlingelnbergCycloPalloidConicalGearSetGearWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_gear_whine_analysis(self) -> 'List[_3842.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis, constructor.new(_3842.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_gear_whine_analysis(self) -> 'List[_3785.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis, constructor.new(_3785.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis))
        return value
