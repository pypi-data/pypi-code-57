'''_5936.py

ConceptGearMeshMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1794
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.system_model.analyses_and_results.mbd_analyses import _5960
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ConceptGearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshMultiBodyDynamicsAnalysis',)


class ConceptGearMeshMultiBodyDynamicsAnalysis(_5960.GearMeshMultiBodyDynamicsAnalysis):
    '''ConceptGearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1794.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1794.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2234.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
