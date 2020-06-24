'''_81.py

NamedDatabaseItem
'''


from mastapy._internal import constructor
from mastapy.utility import _1264
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NAMED_DATABASE_ITEM = python_net_import('SMT.MastaAPI.Utility.Databases', 'NamedDatabaseItem')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedDatabaseItem',)


class NamedDatabaseItem(_1.APIBase):
    '''NamedDatabaseItem

    This is a mastapy class.
    '''

    TYPE = _NAMED_DATABASE_ITEM
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NamedDatabaseItem.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def comment(self) -> 'str':
        '''str: 'Comment' is the original name of this property.'''

        return self.wrapped.Comment

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value else None

    @property
    def no_history(self) -> 'str':
        '''str: 'NoHistory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NoHistory

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def history(self) -> '_1264.FileHistory':
        '''FileHistory: 'History' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1264.FileHistory)(self.wrapped.History) if self.wrapped.History else None
