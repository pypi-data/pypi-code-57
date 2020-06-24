'''_4158.py

ConceptGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1794
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.gears.rating.concept import _551
from mastapy.system_model.analyses_and_results.power_flows import _4173
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshPowerFlow',)


class ConceptGearMeshPowerFlow(_4173.GearMeshPowerFlow):
    '''ConceptGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshPowerFlow.TYPE'):
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

    @property
    def rating(self) -> '_551.ConceptGearMeshRating':
        '''ConceptGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_551.ConceptGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_551.ConceptGearMeshRating':
        '''ConceptGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_551.ConceptGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
