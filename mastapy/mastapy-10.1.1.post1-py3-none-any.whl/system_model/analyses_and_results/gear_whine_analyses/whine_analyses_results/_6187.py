'''_6187.py

ResultNodeSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RESULT_NODE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ResultNodeSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultNodeSelection',)


class ResultNodeSelection(_1.APIBase):
    '''ResultNodeSelection

    This is a mastapy class.
    '''

    TYPE = _RESULT_NODE_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultNodeSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_shown(self) -> 'bool':
        '''bool: 'IsShown' is the original name of this property.'''

        return self.wrapped.IsShown

    @is_shown.setter
    def is_shown(self, value: 'bool'):
        self.wrapped.IsShown = bool(value) if value else False

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def add_to_selected_group(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddToSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddToSelectedGroup

    @property
    def remove_from_selected_group(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveFromSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveFromSelectedGroup

    @property
    def is_in_selected_group(self) -> 'bool':
        '''bool: 'IsInSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInSelectedGroup
