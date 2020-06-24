'''_5463.py

HypoidGearMeshSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1876
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6134
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5410
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'HypoidGearMeshSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshSingleMeshWhineAnalysis',)


class HypoidGearMeshSingleMeshWhineAnalysis(_5410.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis):
    '''HypoidGearMeshSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1876.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1876.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6134.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6134.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
