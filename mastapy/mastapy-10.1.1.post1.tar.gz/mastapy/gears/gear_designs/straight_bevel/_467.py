'''_467.py

StraightBevelGearDesign
'''


from mastapy.gears.gear_designs.bevel import _968
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.StraightBevel', 'StraightBevelGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearDesign',)


class StraightBevelGearDesign(_968.BevelGearDesign):
    '''StraightBevelGearDesign

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
