'''_560.py

CylindricalGearProfileMeasurement
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PROFILE_MEASUREMENT = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearProfileMeasurement')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearProfileMeasurement',)


class CylindricalGearProfileMeasurement(_1.APIBase):
    '''CylindricalGearProfileMeasurement

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_PROFILE_MEASUREMENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearProfileMeasurement.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def diameter(self) -> 'float':
        '''float: 'Diameter' is the original name of this property.'''

        return self.wrapped.Diameter

    @diameter.setter
    def diameter(self, value: 'float'):
        self.wrapped.Diameter = float(value) if value else 0.0

    @property
    def rolling_distance(self) -> 'float':
        '''float: 'RollingDistance' is the original name of this property.'''

        return self.wrapped.RollingDistance

    @rolling_distance.setter
    def rolling_distance(self, value: 'float'):
        self.wrapped.RollingDistance = float(value) if value else 0.0

    @property
    def radius(self) -> 'float':
        '''float: 'Radius' is the original name of this property.'''

        return self.wrapped.Radius

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0

    @property
    def roll_angle(self) -> 'float':
        '''float: 'RollAngle' is the original name of this property.'''

        return self.wrapped.RollAngle

    @roll_angle.setter
    def roll_angle(self, value: 'float'):
        self.wrapped.RollAngle = float(value) if value else 0.0

    @property
    def auto_diameter_show_depending_on_settings(self) -> 'float':
        '''float: 'AutoDiameterShowDependingOnSettings' is the original name of this property.'''

        return self.wrapped.AutoDiameterShowDependingOnSettings

    @auto_diameter_show_depending_on_settings.setter
    def auto_diameter_show_depending_on_settings(self, value: 'float'):
        self.wrapped.AutoDiameterShowDependingOnSettings = float(value) if value else 0.0

    @property
    def auto_radius_show_depending_on_settings(self) -> 'float':
        '''float: 'AutoRadiusShowDependingOnSettings' is the original name of this property.'''

        return self.wrapped.AutoRadiusShowDependingOnSettings

    @auto_radius_show_depending_on_settings.setter
    def auto_radius_show_depending_on_settings(self, value: 'float'):
        self.wrapped.AutoRadiusShowDependingOnSettings = float(value) if value else 0.0

    @property
    def auto_rolling_distance_show_depending_on_settings(self) -> 'float':
        '''float: 'AutoRollingDistanceShowDependingOnSettings' is the original name of this property.'''

        return self.wrapped.AutoRollingDistanceShowDependingOnSettings

    @auto_rolling_distance_show_depending_on_settings.setter
    def auto_rolling_distance_show_depending_on_settings(self, value: 'float'):
        self.wrapped.AutoRollingDistanceShowDependingOnSettings = float(value) if value else 0.0

    @property
    def auto_roll_angle_show_depending_on_settings(self) -> 'float':
        '''float: 'AutoRollAngleShowDependingOnSettings' is the original name of this property.'''

        return self.wrapped.AutoRollAngleShowDependingOnSettings

    @auto_roll_angle_show_depending_on_settings.setter
    def auto_roll_angle_show_depending_on_settings(self, value: 'float'):
        self.wrapped.AutoRollAngleShowDependingOnSettings = float(value) if value else 0.0
