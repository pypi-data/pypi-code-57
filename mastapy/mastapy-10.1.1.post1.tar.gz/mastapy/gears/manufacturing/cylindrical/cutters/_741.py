'''_741.py

CurveInLinkedList
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CURVE_IN_LINKED_LIST = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CurveInLinkedList')


__docformat__ = 'restructuredtext en'
__all__ = ('CurveInLinkedList',)


class CurveInLinkedList(_1.APIBase):
    '''CurveInLinkedList

    This is a mastapy class.
    '''

    TYPE = _CURVE_IN_LINKED_LIST
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CurveInLinkedList.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
