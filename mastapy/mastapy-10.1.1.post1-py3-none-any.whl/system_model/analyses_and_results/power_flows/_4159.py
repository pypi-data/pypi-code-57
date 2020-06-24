'''_4159.py

FaceGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1800
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2236
from mastapy.gears.rating.face import _469
from mastapy.system_model.analyses_and_results.power_flows import _4173
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FaceGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshPowerFlow',)


class FaceGearMeshPowerFlow(_4173.GearMeshPowerFlow):
    '''FaceGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2236.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_469.FaceGearMeshRating':
        '''FaceGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_469.FaceGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_469.FaceGearMeshRating':
        '''FaceGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_469.FaceGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
