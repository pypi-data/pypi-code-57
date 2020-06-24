'''_6507.py

ScriptingCommand
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_SCRIPTING_COMMAND = python_net_import('SMT.MastaAPIUtility.Scripting', 'ScriptingCommand')


__docformat__ = 'restructuredtext en'
__all__ = ('ScriptingCommand',)


class ScriptingCommand:
    '''ScriptingCommand

    This is a mastapy class.
    '''

    TYPE = _SCRIPTING_COMMAND

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ScriptingCommand.TYPE'):
        self.wrapped = instance_to_wrap

    def execute(self):
        ''' 'Execute' is the original name of this method.'''

        self.wrapped.Execute()

    def initialize_lifetime_service(self) -> 'object':
        ''' 'InitializeLifetimeService' is the original name of this method.

        Returns:
            object
        '''

        method_result = self.wrapped.InitializeLifetimeService()
        return method_result
