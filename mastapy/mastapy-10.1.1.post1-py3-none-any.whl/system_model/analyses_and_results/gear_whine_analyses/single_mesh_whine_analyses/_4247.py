'''_4247.py

ConceptGearMeshSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1794
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4262
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ConceptGearMeshSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshSingleMeshWhineAnalysis',)


class ConceptGearMeshSingleMeshWhineAnalysis(_4262.GearMeshSingleMeshWhineAnalysis):
    '''ConceptGearMeshSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshSingleMeshWhineAnalysis.TYPE'):
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
