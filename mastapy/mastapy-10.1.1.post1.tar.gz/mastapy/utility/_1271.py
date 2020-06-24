'''_1271.py

PersistentSingleton
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PERSISTENT_SINGLETON = python_net_import('SMT.MastaAPI.Utility', 'PersistentSingleton')


__docformat__ = 'restructuredtext en'
__all__ = ('PersistentSingleton',)


class PersistentSingleton(_1.APIBase):
    '''PersistentSingleton

    This is a mastapy class.
    '''

    TYPE = _PERSISTENT_SINGLETON
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PersistentSingleton.TYPE'):
        super().__init__(instance_to_wrap)

    def save(self):
        ''' 'Save' is the original name of this method.'''

        self.wrapped.Save()
