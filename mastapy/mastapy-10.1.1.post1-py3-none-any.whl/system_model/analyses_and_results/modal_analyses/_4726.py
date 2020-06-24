'''_4726.py

ConceptGearMeshModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6076
from mastapy.system_model.analyses_and_results.system_deflections import _2235
from mastapy.system_model.analyses_and_results.modal_analyses import _4752
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ConceptGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshModalAnalysis',)


class ConceptGearMeshModalAnalysis(_4752.GearMeshModalAnalysis):
    '''ConceptGearMeshModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6076.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6076.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2235.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2235.ConceptGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
