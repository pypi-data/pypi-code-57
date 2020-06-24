'''_8.py

ConsequenceOfFailure
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONSEQUENCE_OF_FAILURE = python_net_import('SMT.MastaAPI.Shafts', 'ConsequenceOfFailure')


__docformat__ = 'restructuredtext en'
__all__ = ('ConsequenceOfFailure',)


class ConsequenceOfFailure(Enum):
    '''ConsequenceOfFailure

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CONSEQUENCE_OF_FAILURE

    __hash__ = None

    SEVERE = 0
    MEAN = 1
    MODERATE = 2
