'''_1026.py

CylindricalGearMicroGeometryMap
'''


from typing import Callable

from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1045
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _560
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMicroGeometryMap')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometryMap',)


class CylindricalGearMicroGeometryMap(_1.APIBase):
    '''CylindricalGearMicroGeometryMap

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometryMap.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def measured_map_data_type(self) -> '_1045.MeasuredMapDataTypes':
        '''MeasuredMapDataTypes: 'MeasuredMapDataType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MeasuredMapDataType)
        return constructor.new(_1045.MeasuredMapDataTypes)(value) if value else None

    @measured_map_data_type.setter
    def measured_map_data_type(self, value: '_1045.MeasuredMapDataTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MeasuredMapDataType = value

    @property
    def switch_measured_data_direction_with_respect_to_face_width(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SwitchMeasuredDataDirectionWithRespectToFaceWidth' is the original name of this property.'''

        return self.wrapped.SwitchMeasuredDataDirectionWithRespectToFaceWidth

    @switch_measured_data_direction_with_respect_to_face_width.setter
    def switch_measured_data_direction_with_respect_to_face_width(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.SwitchMeasuredDataDirectionWithRespectToFaceWidth = value

    @property
    def profile_factor_for_0_bias_relief(self) -> 'float':
        '''float: 'ProfileFactorFor0BiasRelief' is the original name of this property.'''

        return self.wrapped.ProfileFactorFor0BiasRelief

    @profile_factor_for_0_bias_relief.setter
    def profile_factor_for_0_bias_relief(self, value: 'float'):
        self.wrapped.ProfileFactorFor0BiasRelief = float(value) if value else 0.0

    @property
    def zero_bias_relief(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ZeroBiasRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.ZeroBiasRelief) if self.wrapped.ZeroBiasRelief else None
