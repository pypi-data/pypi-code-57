'''_200.py

FENodeSelectionDrawStyle
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_NODE_SELECTION_DRAW_STYLE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FENodeSelectionDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('FENodeSelectionDrawStyle',)


class FENodeSelectionDrawStyle(_1.APIBase):
    '''FENodeSelectionDrawStyle

    This is a mastapy class.
    '''

    TYPE = _FE_NODE_SELECTION_DRAW_STYLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FENodeSelectionDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_to_selection(self) -> 'bool':
        '''bool: 'AddToSelection' is the original name of this property.'''

        return self.wrapped.AddToSelection

    @add_to_selection.setter
    def add_to_selection(self, value: 'bool'):
        self.wrapped.AddToSelection = bool(value) if value else False

    @property
    def clear_selection(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearSelection' is the original name of this property.'''

        return self.wrapped.ClearSelection

    @clear_selection.setter
    def clear_selection(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.ClearSelection = value

    @property
    def region_size(self) -> 'float':
        '''float: 'RegionSize' is the original name of this property.'''

        return self.wrapped.RegionSize

    @region_size.setter
    def region_size(self, value: 'float'):
        self.wrapped.RegionSize = float(value) if value else 0.0
