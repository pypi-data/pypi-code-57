'''_1363.py

CouplingType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COUPLING_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'CouplingType')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingType',)


class CouplingType(Enum):
    '''CouplingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _COUPLING_TYPE

    __hash__ = None

    DISPLACEMENT = 0
    VELOCITY = 1
