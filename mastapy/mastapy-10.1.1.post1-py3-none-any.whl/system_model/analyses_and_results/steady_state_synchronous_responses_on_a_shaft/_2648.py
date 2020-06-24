'''_2648.py

BevelGearMeshSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets.gears import (
    _1792, _1790, _1812, _1814,
    _1816, _1820
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2636
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BevelGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshSteadyStateSynchronousResponseOnAShaft',)


class BevelGearMeshSteadyStateSynchronousResponseOnAShaft(_2636.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft):
    '''BevelGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1792.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1792.BevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'BevelDifferentialGearMesh':
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1812.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'SpiralBevelGearMesh':
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1812.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelDiffGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ZerolBevelGearMesh':
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
