'''_1047.py

MeshedCylindricalGearMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1046
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MESHED_CYLINDRICAL_GEAR_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'MeshedCylindricalGearMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshedCylindricalGearMicroGeometry',)


class MeshedCylindricalGearMicroGeometry(_1.APIBase):
    '''MeshedCylindricalGearMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _MESHED_CYLINDRICAL_GEAR_MICRO_GEOMETRY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeshedCylindricalGearMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flanks(self) -> 'List[_1046.MeshedCylindricalGearFlankMicroGeometry]':
        '''List[MeshedCylindricalGearFlankMicroGeometry]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Flanks, constructor.new(_1046.MeshedCylindricalGearFlankMicroGeometry))
        return value
