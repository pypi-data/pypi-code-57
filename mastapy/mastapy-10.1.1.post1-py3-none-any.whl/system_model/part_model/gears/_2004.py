'''_2004.py

SpiralBevelGear
'''


from mastapy.gears.gear_designs.spiral_bevel import _442
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2001
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGear',)


class SpiralBevelGear(_2001.BevelGear):
    '''SpiralBevelGear

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bevel_gear_design(self) -> '_442.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_442.SpiralBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def spiral_bevel_gear_design(self) -> '_442.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'SpiralBevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_442.SpiralBevelGearDesign)(self.wrapped.SpiralBevelGearDesign) if self.wrapped.SpiralBevelGearDesign else None
