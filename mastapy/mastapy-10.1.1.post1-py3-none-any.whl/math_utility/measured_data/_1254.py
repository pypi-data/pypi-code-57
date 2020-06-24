'''_1254.py

LookupTableBase
'''


from typing import Generic, TypeVar

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1222
from mastapy._internal import constructor
from mastapy.utility import _334
from mastapy._internal.python_net import python_net_import

_LOOKUP_TABLE_BASE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'LookupTableBase')


__docformat__ = 'restructuredtext en'
__all__ = ('LookupTableBase',)


T = TypeVar('T', bound='')


class LookupTableBase(_334.IndependentReportablePropertiesBase['T'], Generic[T]):
    '''LookupTableBase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _LOOKUP_TABLE_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LookupTableBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def extrapolation_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions':
        '''enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions: 'ExtrapolationOption' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions)(self.wrapped.ExtrapolationOption) if self.wrapped.ExtrapolationOption else None

    @extrapolation_option.setter
    def extrapolation_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ExtrapolationOption = value
