'''_1661.py

CylindricalRollerBearing
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1695
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'CylindricalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalRollerBearing',)


class CylindricalRollerBearing(_1695.NonBarrelRollerBearing):
    '''CylindricalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def iso2812007e_limiting_value_for_dynamic_equivalent_load(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISO2812007ELimitingValueForDynamicEquivalentLoad' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISO2812007ELimitingValueForDynamicEquivalentLoad) if self.wrapped.ISO2812007ELimitingValueForDynamicEquivalentLoad else None

    @iso2812007e_limiting_value_for_dynamic_equivalent_load.setter
    def iso2812007e_limiting_value_for_dynamic_equivalent_load(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISO2812007ELimitingValueForDynamicEquivalentLoad = value

    @property
    def reference_rotation_speed(self) -> 'float':
        '''float: 'ReferenceRotationSpeed' is the original name of this property.'''

        return self.wrapped.ReferenceRotationSpeed

    @reference_rotation_speed.setter
    def reference_rotation_speed(self, value: 'float'):
        self.wrapped.ReferenceRotationSpeed = float(value) if value else 0.0
