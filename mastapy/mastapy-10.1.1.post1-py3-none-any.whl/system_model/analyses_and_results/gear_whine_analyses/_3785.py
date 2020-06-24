'''_3785.py

KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1809
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2252
from mastapy.system_model.analyses_and_results.system_deflections import _2251
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3783
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis(_3783.KlingelnbergCycloPalloidConicalGearMeshGearWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
