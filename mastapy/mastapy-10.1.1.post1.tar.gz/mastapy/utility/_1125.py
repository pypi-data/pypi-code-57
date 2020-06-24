'''_1125.py

Command
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_COMMAND = python_net_import('SMT.MastaAPI.Utility', 'Command')


__docformat__ = 'restructuredtext en'
__all__ = ('Command',)


class Command:
    '''Command

    This is a mastapy class.
    '''

    TYPE = _COMMAND

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Command.TYPE'):
        self.wrapped = instance_to_wrap

    def run(self):
        ''' 'Run' is the original name of this method.'''

        self.wrapped.Run()

    def initialize_lifetime_service(self) -> 'object':
        ''' 'InitializeLifetimeService' is the original name of this method.

        Returns:
            object
        '''

        method_result = self.wrapped.InitializeLifetimeService()
        return method_result
