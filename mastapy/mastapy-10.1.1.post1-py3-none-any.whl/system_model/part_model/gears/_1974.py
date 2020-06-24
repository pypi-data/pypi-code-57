'''_1974.py

BevelDifferentialGear
'''


from mastapy.gears.gear_designs.bevel import _1039
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _427
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _452
from mastapy.gears.gear_designs.straight_bevel import _445
from mastapy.gears.gear_designs.spiral_bevel import _454
from mastapy.system_model.part_model.gears import _1978
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGear',)


class BevelDifferentialGear(_1978.BevelGear):
    '''BevelDifferentialGear

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bevel_gear_design(self) -> '_1039.BevelGearDesign':
        '''BevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1039.BevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_zerol_bevel_gear_design(self) -> '_427.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearDesign.__class__.__qualname__ != 'ZerolBevelGearDesign':
            raise CastException('Failed to cast bevel_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_427.ZerolBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_452.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearDesign.__class__.__qualname__ != 'StraightBevelDiffGearDesign':
            raise CastException('Failed to cast bevel_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_452.StraightBevelDiffGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_gear_design(self) -> '_445.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearDesign.__class__.__qualname__ != 'StraightBevelGearDesign':
            raise CastException('Failed to cast bevel_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_445.StraightBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_spiral_bevel_gear_design(self) -> '_454.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BevelGearDesign.__class__.__qualname__ != 'SpiralBevelGearDesign':
            raise CastException('Failed to cast bevel_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_454.SpiralBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None
