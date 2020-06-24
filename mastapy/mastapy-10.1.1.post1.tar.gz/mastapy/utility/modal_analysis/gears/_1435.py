'''_1435.py

OrderForTE
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ORDER_FOR_TE = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'OrderForTE')


__docformat__ = 'restructuredtext en'
__all__ = ('OrderForTE',)


class OrderForTE(_1.APIBase):
    '''OrderForTE

    This is a mastapy class.
    '''

    TYPE = _ORDER_FOR_TE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OrderForTE.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def order(self) -> 'float':
        '''float: 'Order' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Order

    @property
    def frequency_offset(self) -> 'float':
        '''float: 'FrequencyOffset' is the original name of this property.'''

        return self.wrapped.FrequencyOffset

    @frequency_offset.setter
    def frequency_offset(self, value: 'float'):
        self.wrapped.FrequencyOffset = float(value) if value else 0.0
