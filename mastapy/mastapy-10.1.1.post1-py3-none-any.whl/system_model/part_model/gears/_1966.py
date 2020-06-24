'''_1966.py

SpiralBevelGearSet
'''


from typing import List

from mastapy.gears.gear_designs.spiral_bevel import _395
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2004, _1980
from mastapy.system_model.connections_and_sockets.gears import _1812
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSet',)


class SpiralBevelGearSet(_1980.BevelGearSet):
    '''SpiralBevelGearSet

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def spiral_bevel_gear_set_design(self) -> '_395.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SpiralBevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_395.SpiralBevelGearSetDesign)(self.wrapped.SpiralBevelGearSetDesign) if self.wrapped.SpiralBevelGearSetDesign else None

    @property
    def spiral_bevel_gears(self) -> 'List[_2004.SpiralBevelGear]':
        '''List[SpiralBevelGear]: 'SpiralBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGears, constructor.new(_2004.SpiralBevelGear))
        return value

    @property
    def spiral_bevel_meshes(self) -> 'List[_1812.SpiralBevelGearMesh]':
        '''List[SpiralBevelGearMesh]: 'SpiralBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshes, constructor.new(_1812.SpiralBevelGearMesh))
        return value
