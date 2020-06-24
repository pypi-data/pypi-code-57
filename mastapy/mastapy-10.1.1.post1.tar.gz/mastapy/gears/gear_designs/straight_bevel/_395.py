'''_395.py

StraightBevelGearSetDesign
'''


from typing import List

from mastapy.gears.gear_designs.straight_bevel import _467, _446
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.bevel import _963
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.StraightBevel', 'StraightBevelGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetDesign',)


class StraightBevelGearSetDesign(_963.BevelGearSetDesign):
    '''StraightBevelGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gears(self) -> 'List[_467.StraightBevelGearDesign]':
        '''List[StraightBevelGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_467.StraightBevelGearDesign))
        return value

    @property
    def straight_bevel_gears(self) -> 'List[_467.StraightBevelGearDesign]':
        '''List[StraightBevelGearDesign]: 'StraightBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGears, constructor.new(_467.StraightBevelGearDesign))
        return value

    @property
    def straight_bevel_meshes(self) -> 'List[_446.StraightBevelGearMeshDesign]':
        '''List[StraightBevelGearMeshDesign]: 'StraightBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshes, constructor.new(_446.StraightBevelGearMeshDesign))
        return value
