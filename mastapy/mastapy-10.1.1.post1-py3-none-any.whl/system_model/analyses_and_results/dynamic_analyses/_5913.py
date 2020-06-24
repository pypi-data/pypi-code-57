'''_5913.py

WormGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1890
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6210
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5849
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'WormGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshDynamicAnalysis',)


class WormGearMeshDynamicAnalysis(_5849.GearMeshDynamicAnalysis):
    '''WormGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1890.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1890.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6210.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6210.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
