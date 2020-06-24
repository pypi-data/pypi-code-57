'''_1727.py

ExternalFullFELoader
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_EXTERNAL_FULL_FE_LOADER = python_net_import('SMT.MastaAPI.SystemModel', 'ExternalFullFELoader')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalFullFELoader',)


class ExternalFullFELoader(_1.APIBase):
    '''ExternalFullFELoader

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_FULL_FE_LOADER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalFullFELoader.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_full_fe_for(self) -> 'str':
        '''str: 'LoadFullFEFor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadFullFEFor
