'''_5341.py

KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2080
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6147
from mastapy.system_model.analyses_and_results.system_deflections import _2283
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5339, _5340, _5335
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis(_5335.KlingelnbergCycloPalloidConicalGearSetGearWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2080.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6147.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6147.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2283.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5339.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5339.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_gear_whine_analysis(self) -> 'List[_5339.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis, constructor.new(_5339.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5340.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5340.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_gear_whine_analysis(self) -> 'List[_5340.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis, constructor.new(_5340.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis))
        return value
