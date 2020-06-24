'''_1475.py

DegreeOfFreedomType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'DegreeOfFreedomType')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreeOfFreedomType',)


class DegreeOfFreedomType(Enum):
    '''DegreeOfFreedomType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DEGREE_OF_FREEDOM_TYPE

    __hash__ = None

    INDEPENDENT = 0
    DEPENDENT = 1
