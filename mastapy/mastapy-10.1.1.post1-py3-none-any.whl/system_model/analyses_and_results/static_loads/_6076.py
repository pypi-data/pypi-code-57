'''_6076.py

ConceptGearMeshLoadCase
'''


from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6120
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshLoadCase',)


class ConceptGearMeshLoadCase(_6120.GearMeshLoadCase):
    '''ConceptGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
