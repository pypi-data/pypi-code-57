'''_1981.py

BevelDifferentialGearSet
'''


from typing import List

from mastapy.gears.gear_designs.bevel import _1036
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _392
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _393
from mastapy.gears.gear_designs.straight_bevel import _394
from mastapy.gears.gear_designs.spiral_bevel import _395
from mastapy.system_model.part_model.gears import _2001, _1980
from mastapy.system_model.connections_and_sockets.gears import _1792
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSet',)


class BevelDifferentialGearSet(_1980.BevelGearSet):
    '''BevelDifferentialGearSet

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_set_design(self) -> '_1036.BevelGearSetDesign':
        '''BevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1036.BevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_392.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'ZerolBevelGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_392.ZerolBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_393.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'StraightBevelDiffGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_393.StraightBevelDiffGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_394.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'StraightBevelGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_394.StraightBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConicalGearSetDesign.__class__.__qualname__ != 'SpiralBevelGearSetDesign':
            raise CastException('Failed to cast conical_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def bevel_gear_set_design(self) -> '_1036.BevelGearSetDesign':
        '''BevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1036.BevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_392.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearSetDesign.__class__.__qualname__ != 'ZerolBevelGearSetDesign':
            raise CastException('Failed to cast bevel_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_392.ZerolBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_393.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearSetDesign.__class__.__qualname__ != 'StraightBevelDiffGearSetDesign':
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_393.StraightBevelDiffGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_394.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearSetDesign.__class__.__qualname__ != 'StraightBevelGearSetDesign':
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_394.StraightBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearSetDesign.__class__.__qualname__ != 'SpiralBevelGearSetDesign':
            raise CastException('Failed to cast bevel_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gears(self) -> 'List[_2001.BevelGear]':
        '''List[BevelGear]: 'BevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelGears, constructor.new(_2001.BevelGear))
        return value

    @property
    def bevel_meshes(self) -> 'List[_1792.BevelGearMesh]':
        '''List[BevelGearMesh]: 'BevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelMeshes, constructor.new(_1792.BevelGearMesh))
        return value
