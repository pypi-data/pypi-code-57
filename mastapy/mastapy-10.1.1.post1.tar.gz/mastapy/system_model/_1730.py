'''_1730.py

MemorySummary
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MEMORY_SUMMARY = python_net_import('SMT.MastaAPI.SystemModel', 'MemorySummary')


__docformat__ = 'restructuredtext en'
__all__ = ('MemorySummary',)


class MemorySummary(_1.APIBase):
    '''MemorySummary

    This is a mastapy class.
    '''

    TYPE = _MEMORY_SUMMARY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MemorySummary.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def force_garbage_collection(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ForceGarbageCollection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceGarbageCollection

    @property
    def current_gc_memory_usage(self) -> 'str':
        '''str: 'CurrentGCMemoryUsage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentGCMemoryUsage

    @property
    def virtual_memory_size(self) -> 'str':
        '''str: 'VirtualMemorySize' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VirtualMemorySize

    @property
    def garbage_collections(self) -> 'str':
        '''str: 'GarbageCollections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GarbageCollections
