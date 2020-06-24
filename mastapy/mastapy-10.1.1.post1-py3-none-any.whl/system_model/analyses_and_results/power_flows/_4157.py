'''_4157.py

BevelDifferentialGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1790
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2233
from mastapy.gears.rating.bevel import _426
from mastapy.gears.rating.zerol_bevel import _348
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.straight_bevel import _413
from mastapy.gears.rating.spiral_bevel import _415
from mastapy.system_model.analyses_and_results.power_flows import _4161
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BevelDifferentialGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshPowerFlow',)


class BevelDifferentialGearMeshPowerFlow(_4161.BevelGearMeshPowerFlow):
    '''BevelDifferentialGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshPowerFlow.TYPE'):
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

    @property
    def rating(self) -> '_426.BevelGearMeshRating':
        '''BevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_426.BevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_mesh_rating(self) -> '_348.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'ZerolBevelGearMeshRating':
            raise CastException('Failed to cast rating to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_348.ZerolBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_mesh_rating(self) -> '_413.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'StraightBevelGearMeshRating':
            raise CastException('Failed to cast rating to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_413.StraightBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_mesh_rating(self) -> '_415.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Rating.__class__.__qualname__ != 'SpiralBevelGearMeshRating':
            raise CastException('Failed to cast rating to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new(_415.SpiralBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_426.BevelGearMeshRating':
        '''BevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_426.BevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_zerol_bevel_gear_mesh_rating(self) -> '_348.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'ZerolBevelGearMeshRating':
            raise CastException('Failed to cast component_detailed_analysis to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_348.ZerolBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_straight_bevel_gear_mesh_rating(self) -> '_413.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'StraightBevelGearMeshRating':
            raise CastException('Failed to cast component_detailed_analysis to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_413.StraightBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spiral_bevel_gear_mesh_rating(self) -> '_415.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'SpiralBevelGearMeshRating':
            raise CastException('Failed to cast component_detailed_analysis to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_415.SpiralBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
