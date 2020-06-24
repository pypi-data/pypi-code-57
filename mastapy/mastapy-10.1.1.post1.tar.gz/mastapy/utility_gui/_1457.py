'''_1457.py

DataInputFileOptions
'''


from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DATA_INPUT_FILE_OPTIONS = python_net_import('SMT.MastaAPI.UtilityGUI', 'DataInputFileOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DataInputFileOptions',)


class DataInputFileOptions(_1.APIBase):
    '''DataInputFileOptions

    This is a mastapy class.
    '''

    TYPE = _DATA_INPUT_FILE_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DataInputFileOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def sheet(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'Sheet' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.Sheet) if self.wrapped.Sheet else None

    @sheet.setter
    def sheet(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.Sheet = value

    @property
    def column_headers_row(self) -> 'int':
        '''int: 'ColumnHeadersRow' is the original name of this property.'''

        return self.wrapped.ColumnHeadersRow

    @column_headers_row.setter
    def column_headers_row(self, value: 'int'):
        self.wrapped.ColumnHeadersRow = int(value) if value else 0

    @property
    def data_start_row(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'DataStartRow' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.DataStartRow) if self.wrapped.DataStartRow else None

    @data_start_row.setter
    def data_start_row(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.DataStartRow = value

    @property
    def data_end_row(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'DataEndRow' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.DataEndRow) if self.wrapped.DataEndRow else None

    @data_end_row.setter
    def data_end_row(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.DataEndRow = value

    @property
    def selected_file_name(self) -> 'str':
        '''str: 'SelectedFileName' is the original name of this property.'''

        return self.wrapped.SelectedFileName

    @selected_file_name.setter
    def selected_file_name(self, value: 'str'):
        self.wrapped.SelectedFileName = str(value) if value else None

    def open_file(self, filename: 'str'):
        ''' 'OpenFile' is the original name of this method.

        Args:
            filename (str)
        '''

        filename = str(filename)
        self.wrapped.OpenFile(filename if filename else None)
