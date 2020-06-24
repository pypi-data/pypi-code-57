'''_2235.py

ConceptGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6076
from mastapy.system_model.analyses_and_results.power_flows import _3243
from mastapy.gears.rating.concept import _335
from mastapy.system_model.analyses_and_results.system_deflections import _2267
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshSystemDeflection',)


class ConceptGearMeshSystemDeflection(_2267.GearMeshSystemDeflection):
    '''ConceptGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshSystemDeflection.TYPE'):
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
    def power_flow_results(self) -> '_3243.ConceptGearMeshPowerFlow':
        '''ConceptGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3243.ConceptGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_335.ConceptGearMeshRating':
        '''ConceptGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_335.ConceptGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_335.ConceptGearMeshRating':
        '''ConceptGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_335.ConceptGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
