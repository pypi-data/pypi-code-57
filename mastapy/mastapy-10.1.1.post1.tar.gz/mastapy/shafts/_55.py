'''_55.py

ShaftProfile
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.shafts import _56
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_PROFILE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftProfile',)


class ShaftProfile(_1.APIBase):
    '''ShaftProfile

    This is a mastapy class.
    '''

    TYPE = _SHAFT_PROFILE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftProfile.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Add' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Add

    @property
    def import_from_clipboard(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportFromClipboard' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportFromClipboard

    @property
    def add_for_context_menu(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddForContextMenu' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddForContextMenu

    @property
    def points(self) -> 'List[_56.ShaftProfilePoint]':
        '''List[ShaftProfilePoint]: 'Points' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Points, constructor.new(_56.ShaftProfilePoint))
        return value

    def make_valid(self):
        ''' 'MakeValid' is the original name of this method.'''

        self.wrapped.MakeValid()

    def add_profile_point(self, offset: 'float', diameter: 'float'):
        ''' 'AddProfilePoint' is the original name of this method.

        Args:
            offset (float)
            diameter (float)
        '''

        offset = float(offset)
        diameter = float(diameter)
        self.wrapped.AddProfilePoint(offset if offset else 0.0, diameter if diameter else 0.0)

    def clear(self):
        ''' 'Clear' is the original name of this method.'''

        self.wrapped.Clear()
