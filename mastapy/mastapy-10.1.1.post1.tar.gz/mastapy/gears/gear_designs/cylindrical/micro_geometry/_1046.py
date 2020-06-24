'''_1046.py

MeshedCylindricalGearFlankMicroGeometry
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1054, _1049
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MESHED_CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'MeshedCylindricalGearFlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshedCylindricalGearFlankMicroGeometry',)


class MeshedCylindricalGearFlankMicroGeometry(_1.APIBase):
    '''MeshedCylindricalGearFlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _MESHED_CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeshedCylindricalGearFlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def total_profile_relief_points(self) -> 'List[_1054.TotalProfileReliefWithDeviation]':
        '''List[TotalProfileReliefWithDeviation]: 'TotalProfileReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TotalProfileReliefPoints, constructor.new(_1054.TotalProfileReliefWithDeviation))
        return value

    @property
    def profile_form_relief_points(self) -> 'List[_1049.ProfileFormReliefWithDeviation]':
        '''List[ProfileFormReliefWithDeviation]: 'ProfileFormReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileFormReliefPoints, constructor.new(_1049.ProfileFormReliefWithDeviation))
        return value

    @property
    def involute_inspection_points(self) -> 'List[_1054.TotalProfileReliefWithDeviation]':
        '''List[TotalProfileReliefWithDeviation]: 'InvoluteInspectionPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InvoluteInspectionPoints, constructor.new(_1054.TotalProfileReliefWithDeviation))
        return value
