'''_973.py

CylindricalGearDesignConstraint
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.model_validation import _1102
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINT = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraint')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraint',)


class CylindricalGearDesignConstraint(_1.APIBase):
    '''CylindricalGearDesignConstraint

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraint.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_active(self) -> 'bool':
        '''bool: 'IsActive' is the original name of this property.'''

        return self.wrapped.IsActive

    @is_active.setter
    def is_active(self, value: 'bool'):
        self.wrapped.IsActive = bool(value) if value else False

    @property
    def class_of_error(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity':
        '''enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity: 'ClassOfError' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity)(self.wrapped.ClassOfError) if self.wrapped.ClassOfError else None

    @class_of_error.setter
    def class_of_error(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ClassOfError = value

    @property
    def property_(self) -> 'str':
        '''str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Property

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete
