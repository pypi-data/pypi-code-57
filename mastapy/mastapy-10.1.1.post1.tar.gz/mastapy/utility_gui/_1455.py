'''_1455.py

MASTAGUI
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model import _1719
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MASTAGUI = python_net_import('SMT.MastaAPI.UtilityGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_1.APIBase):
    '''MASTAGUI

    This is a mastapy class.
    '''

    TYPE = _MASTAGUI
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def resume(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Resume' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Resume

    @property
    def is_paused(self) -> 'bool':
        '''bool: 'IsPaused' is the original name of this property.'''

        return self.wrapped.IsPaused

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def pause(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Pause' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Pause

    def open_design_in_new_tab(self, design: '_1719.Design'):
        ''' 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        '''

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def select_tab(self, tab_text: 'str'):
        ''' 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        '''

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else None)
