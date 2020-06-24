'''_1295.py

CustomReportPropertyItem
'''


from mastapy.utility.report import _1306, _1305
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.reporting_property_framework import _1266
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_PROPERTY_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportPropertyItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportPropertyItem',)


class CustomReportPropertyItem(_0.APIBase):
    '''CustomReportPropertyItem

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_REPORT_PROPERTY_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomReportPropertyItem.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def font_weight(self) -> '_1306.FontWeight':
        '''FontWeight: 'FontWeight' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FontWeight)
        return constructor.new(_1306.FontWeight)(value) if value else None

    @font_weight.setter
    def font_weight(self, value: '_1306.FontWeight'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FontWeight = value

    @property
    def font_style(self) -> '_1305.FontStyle':
        '''FontStyle: 'FontStyle' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FontStyle)
        return constructor.new(_1305.FontStyle)(value) if value else None

    @font_style.setter
    def font_style(self, value: '_1305.FontStyle'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FontStyle = value

    @property
    def horizontal_position(self) -> '_1266.CellValuePosition':
        '''CellValuePosition: 'HorizontalPosition' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HorizontalPosition)
        return constructor.new(_1266.CellValuePosition)(value) if value else None

    @horizontal_position.setter
    def horizontal_position(self, value: '_1266.CellValuePosition'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HorizontalPosition = value

    @property
    def show_property_name(self) -> 'bool':
        '''bool: 'ShowPropertyName' is the original name of this property.'''

        return self.wrapped.ShowPropertyName

    @show_property_name.setter
    def show_property_name(self, value: 'bool'):
        self.wrapped.ShowPropertyName = bool(value) if value else False
