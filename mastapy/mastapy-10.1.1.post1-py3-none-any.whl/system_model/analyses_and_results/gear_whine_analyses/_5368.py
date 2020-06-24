'''_5368.py

SpiralBevelGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1884
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6179
from mastapy.system_model.analyses_and_results.system_deflections import _2311
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5268
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SpiralBevelGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshGearWhineAnalysis',)


class SpiralBevelGearMeshGearWhineAnalysis(_5268.BevelGearMeshGearWhineAnalysis):
    '''SpiralBevelGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1884.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1884.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6179.SpiralBevelGearMeshLoadCase':
        '''SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6179.SpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2311.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2311.SpiralBevelGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
