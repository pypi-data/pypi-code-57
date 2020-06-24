'''_1687.py

BarrelRollerBearing
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1696
from mastapy._internal.python_net import python_net_import

_BARREL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BarrelRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('BarrelRollerBearing',)


class BarrelRollerBearing(_1696.RollerBearing):
    '''BarrelRollerBearing

    This is a mastapy class.
    '''

    TYPE = _BARREL_ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BarrelRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def groove_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'GrooveRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.GrooveRadius) if self.wrapped.GrooveRadius else None

    @groove_radius.setter
    def groove_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.GrooveRadius = value

    @property
    def element_profile_radius(self) -> 'float':
        '''float: 'ElementProfileRadius' is the original name of this property.'''

        return self.wrapped.ElementProfileRadius

    @element_profile_radius.setter
    def element_profile_radius(self, value: 'float'):
        self.wrapped.ElementProfileRadius = float(value) if value else 0.0

    @property
    def roller_race_radius_ratio(self) -> 'float':
        '''float: 'RollerRaceRadiusRatio' is the original name of this property.'''

        return self.wrapped.RollerRaceRadiusRatio

    @roller_race_radius_ratio.setter
    def roller_race_radius_ratio(self, value: 'float'):
        self.wrapped.RollerRaceRadiusRatio = float(value) if value else 0.0
