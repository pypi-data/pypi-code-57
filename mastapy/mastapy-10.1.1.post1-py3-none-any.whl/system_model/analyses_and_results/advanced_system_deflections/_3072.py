'''_3072.py

KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1809
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2297
from mastapy.gears.rating.klingelnberg_spiral_bevel import _417
from mastapy.system_model.analyses_and_results.system_deflections import _2211
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3070
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection(_3070.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2297.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2297.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_417.KlingelnbergCycloPalloidSpiralBevelGearMeshRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_417.KlingelnbergCycloPalloidSpiralBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2211.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2211.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection))
        return value
