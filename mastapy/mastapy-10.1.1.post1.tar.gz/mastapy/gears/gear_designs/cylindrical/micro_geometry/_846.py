'''_846.py

CylindricalGearMicroGeometry
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _775, _783
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _841, _861
from mastapy.gears.analysis import _952
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometry',)


class CylindricalGearMicroGeometry(_952.GearImplementationDetail):
    '''CylindricalGearMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_same_micro_geometry_on_both_flanks(self) -> 'bool':
        '''bool: 'UseSameMicroGeometryOnBothFlanks' is the original name of this property.'''

        return self.wrapped.UseSameMicroGeometryOnBothFlanks

    @use_same_micro_geometry_on_both_flanks.setter
    def use_same_micro_geometry_on_both_flanks(self, value: 'bool'):
        self.wrapped.UseSameMicroGeometryOnBothFlanks = bool(value) if value else False

    @property
    def profile_control_point_is_user_specified(self) -> 'bool':
        '''bool: 'ProfileControlPointIsUserSpecified' is the original name of this property.'''

        return self.wrapped.ProfileControlPointIsUserSpecified

    @profile_control_point_is_user_specified.setter
    def profile_control_point_is_user_specified(self, value: 'bool'):
        self.wrapped.ProfileControlPointIsUserSpecified = bool(value) if value else False

    @property
    def cylindrical_gear(self) -> '_775.CylindricalGearDesign':
        '''CylindricalGearDesign: 'CylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_775.CylindricalGearDesign)(self.wrapped.CylindricalGear) if self.wrapped.CylindricalGear else None

    @property
    def left_flank(self) -> '_841.CylindricalGearFlankMicroGeometry':
        '''CylindricalGearFlankMicroGeometry: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_841.CylindricalGearFlankMicroGeometry)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None

    @property
    def right_flank(self) -> '_841.CylindricalGearFlankMicroGeometry':
        '''CylindricalGearFlankMicroGeometry: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_841.CylindricalGearFlankMicroGeometry)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def profile_control_point(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ProfileControlPoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.ProfileControlPoint) if self.wrapped.ProfileControlPoint else None

    @property
    def flanks(self) -> 'List[_841.CylindricalGearFlankMicroGeometry]':
        '''List[CylindricalGearFlankMicroGeometry]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Flanks, constructor.new(_841.CylindricalGearFlankMicroGeometry))
        return value

    @property
    def meshed_gears(self) -> 'List[_861.MeshedCylindricalGearMicroGeometry]':
        '''List[MeshedCylindricalGearMicroGeometry]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_861.MeshedCylindricalGearMicroGeometry))
        return value
