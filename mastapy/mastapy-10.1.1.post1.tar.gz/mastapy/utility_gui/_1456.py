'''_1456.py

ColumnInputOptions
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.utility.file_access_helpers import _1441
from mastapy._internal import constructor
from mastapy.utility.units_and_measurements import _1385
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COLUMN_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.UtilityGUI', 'ColumnInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ColumnInputOptions',)


class ColumnInputOptions(_1.APIBase):
    '''ColumnInputOptions

    This is a mastapy class.
    '''

    TYPE = _COLUMN_INPUT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ColumnInputOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def column(self) -> 'list_with_selected_item.ListWithSelectedItem_ColumnTitle':
        '''list_with_selected_item.ListWithSelectedItem_ColumnTitle: 'Column' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ColumnTitle)(self.wrapped.Column) if self.wrapped.Column else None

    @column.setter
    def column(self, value: 'list_with_selected_item.ListWithSelectedItem_ColumnTitle.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ColumnTitle.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ColumnTitle.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Column = value

    @property
    def unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'Unit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.Unit) if self.wrapped.Unit else None

    @unit.setter
    def unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Unit = value
