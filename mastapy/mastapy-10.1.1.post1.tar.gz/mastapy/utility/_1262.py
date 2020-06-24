'''_1262.py

ExecutableDirectoryCopier
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_EXECUTABLE_DIRECTORY_COPIER = python_net_import('SMT.MastaAPI.Utility', 'ExecutableDirectoryCopier')


__docformat__ = 'restructuredtext en'
__all__ = ('ExecutableDirectoryCopier',)


class ExecutableDirectoryCopier(_1.APIBase):
    '''ExecutableDirectoryCopier

    This is a mastapy class.
    '''

    TYPE = _EXECUTABLE_DIRECTORY_COPIER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExecutableDirectoryCopier.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def message(self) -> 'str':
        '''str: 'Message' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Message

    @property
    def space_required_for_local_copy(self) -> 'str':
        '''str: 'SpaceRequiredForLocalCopy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpaceRequiredForLocalCopy

    @property
    def local_copy_parent_directory(self) -> 'str':
        '''str: 'LocalCopyParentDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LocalCopyParentDirectory

    @property
    def local_copy_found_at(self) -> 'str':
        '''str: 'LocalCopyFoundAt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LocalCopyFoundAt

    @property
    def selected_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option':
        '''enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option: 'SelectedOption' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option)(self.wrapped.SelectedOption) if self.wrapped.SelectedOption else None

    @selected_option.setter
    def selected_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExecutableDirectoryCopier_Option.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.SelectedOption = value
