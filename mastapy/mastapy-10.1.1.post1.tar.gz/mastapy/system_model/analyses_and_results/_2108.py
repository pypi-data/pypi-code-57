'''_2108.py

Context
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONTEXT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'Context')


__docformat__ = 'restructuredtext en'
__all__ = ('Context',)


class Context(_1.APIBase):
    '''Context

    This is a mastapy class.
    '''

    TYPE = _CONTEXT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Context.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None
