'''_1367.py

ElementOrder
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ELEMENT_ORDER = python_net_import('SMT.MastaAPI.NodalAnalysis', 'ElementOrder')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementOrder',)


class ElementOrder(Enum):
    '''ElementOrder

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _ELEMENT_ORDER

    __hash__ = None

    LINEAR = 0
    QUADRATIC = 1
