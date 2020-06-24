'''_1695.py

NonBarrelRollerBearing
'''


from typing import List

from mastapy.bearings.bearing_designs.rolling import _1697, _1698, _1696
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.python_net import python_net_import

_NON_BARREL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'NonBarrelRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('NonBarrelRollerBearing',)


class NonBarrelRollerBearing(_1696.RollerBearing):
    '''NonBarrelRollerBearing

    This is a mastapy class.
    '''

    TYPE = _NON_BARREL_ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NonBarrelRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def roller_end_shape(self) -> '_1697.RollerEndShape':
        '''RollerEndShape: 'RollerEndShape' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RollerEndShape)
        return constructor.new(_1697.RollerEndShape)(value) if value else None

    @roller_end_shape.setter
    def roller_end_shape(self, value: '_1697.RollerEndShape'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RollerEndShape = value

    @property
    def roller_end_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RollerEndRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RollerEndRadius) if self.wrapped.RollerEndRadius else None

    @roller_end_radius.setter
    def roller_end_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RollerEndRadius = value

    @property
    def ribs(self) -> 'List[_1698.RollerRibDetail]':
        '''List[RollerRibDetail]: 'Ribs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Ribs, constructor.new(_1698.RollerRibDetail))
        return value
