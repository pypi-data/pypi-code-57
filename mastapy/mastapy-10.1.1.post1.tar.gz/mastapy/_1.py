'''_1.py

Initialiser
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_INITIALISER = python_net_import('SMT.MastaAPI', 'Initialiser')


__docformat__ = 'restructuredtext en'
__all__ = ('Initialiser',)


class Initialiser:
    '''Initialiser

    This is a mastapy class.
    '''

    TYPE = _INITIALISER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Initialiser.TYPE'):
        self.wrapped = instance_to_wrap

    def initialise_api_access(self, installation_directory: 'str'):
        ''' 'InitialiseApiAccess' is the original name of this method.

        Args:
            installation_directory (str)
        '''

        installation_directory = str(installation_directory)
        self.wrapped.InitialiseApiAccess(installation_directory if installation_directory else None)
