'''_5265.py

StraightBevelDiffGearMeshModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2238
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5181
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelDiffGearMeshModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshModalAnalysesAtSpeeds',)


class StraightBevelDiffGearMeshModalAnalysesAtSpeeds(_5181.BevelGearMeshModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearMeshModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2238.StraightBevelDiffGearMeshLoadCase':
        '''StraightBevelDiffGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2238.StraightBevelDiffGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
