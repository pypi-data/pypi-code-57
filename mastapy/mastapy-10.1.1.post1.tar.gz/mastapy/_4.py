'''_4.py

PythonUtility
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_PYTHON_UTILITY = python_net_import('SMT.MastaAPI', 'PythonUtility')


__docformat__ = 'restructuredtext en'
__all__ = ('PythonUtility',)


class PythonUtility:
    '''PythonUtility

    This is a mastapy class.
    '''

    TYPE = _PYTHON_UTILITY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PythonUtility.TYPE'):
        self.wrapped = instance_to_wrap

    @staticmethod
    def python_install_directory() -> 'str':
        '''str: 'PythonInstallDirectory' is the original name of this method.'''

        return PythonUtility.TYPE.PythonInstallDirectory
