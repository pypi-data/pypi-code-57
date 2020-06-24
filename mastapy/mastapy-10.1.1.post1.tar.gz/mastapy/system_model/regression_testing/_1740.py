'''_1740.py

PerformRegressionTestFromMASTAOptions
'''


from typing import Callable

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PERFORM_REGRESSION_TEST_FROM_MASTA_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.RegressionTesting', 'PerformRegressionTestFromMASTAOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PerformRegressionTestFromMASTAOptions',)


class PerformRegressionTestFromMASTAOptions(_1.APIBase):
    '''PerformRegressionTestFromMASTAOptions

    This is a mastapy class.
    '''

    TYPE = _PERFORM_REGRESSION_TEST_FROM_MASTA_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PerformRegressionTestFromMASTAOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def selected_version(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'SelectedVersion' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.SelectedVersion) if self.wrapped.SelectedVersion else None

    @selected_version.setter
    def selected_version(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.SelectedVersion = value

    @property
    def run(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Run' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Run
