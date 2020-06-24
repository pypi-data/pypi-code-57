'''_1260.py

DispatcherHelper
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DISPATCHER_HELPER = python_net_import('SMT.MastaAPI.Utility', 'DispatcherHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('DispatcherHelper',)


class DispatcherHelper(_1.APIBase):
    '''DispatcherHelper

    This is a mastapy class.
    '''

    TYPE = _DISPATCHER_HELPER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DispatcherHelper.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_suspended(self) -> 'bool':
        '''bool: 'IsSuspended' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsSuspended

    @property
    def disable_processing_count(self) -> 'int':
        '''int: 'DisableProcessingCount' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisableProcessingCount

    @property
    def frame_depth(self) -> 'int':
        '''int: 'FrameDepth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FrameDepth

    @property
    def timers(self) -> 'str':
        '''str: 'Timers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Timers

    @property
    def number_of_queued_items(self) -> 'int':
        '''int: 'NumberOfQueuedItems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfQueuedItems

    @property
    def has_shutdown_started(self) -> 'bool':
        '''bool: 'HasShutdownStarted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasShutdownStarted

    @property
    def has_shutdown_finished(self) -> 'bool':
        '''bool: 'HasShutdownFinished' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasShutdownFinished

    @property
    def thread(self) -> 'str':
        '''str: 'Thread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Thread
