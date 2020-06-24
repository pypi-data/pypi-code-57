'''_5918.py

BevelDifferentialGearMeshMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1790
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2233
from mastapy.system_model.analyses_and_results.mbd_analyses import _5923
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BevelDifferentialGearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshMultiBodyDynamicsAnalysis',)


class BevelDifferentialGearMeshMultiBodyDynamicsAnalysis(_5923.BevelGearMeshMultiBodyDynamicsAnalysis):
    '''BevelDifferentialGearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2233.BevelDifferentialGearMeshLoadCase':
        '''BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2233.BevelDifferentialGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
