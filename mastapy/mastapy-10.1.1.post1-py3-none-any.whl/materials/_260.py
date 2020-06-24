'''_260.py

LubricationDetailDatabase
'''


from typing import Iterable

from mastapy.materials import _259
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LUBRICATION_DETAIL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'LubricationDetailDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('LubricationDetailDatabase',)


class LubricationDetailDatabase(_1.APIBase):
    '''LubricationDetailDatabase

    This is a mastapy class.
    '''

    TYPE = _LUBRICATION_DETAIL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LubricationDetailDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_259.LubricationDetail':
        '''LubricationDetail: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_259.LubricationDetail)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_259.LubricationDetail':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.materials.LubricationDetail
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_259.LubricationDetail)(method_result) if method_result else None

    def can_be_removed(self, lubrication_detail: '_259.LubricationDetail') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            lubrication_detail (mastapy.materials.LubricationDetail)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(lubrication_detail.wrapped if lubrication_detail else None)
        return method_result

    def rename(self, lubrication_detail: '_259.LubricationDetail', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            lubrication_detail (mastapy.materials.LubricationDetail)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(lubrication_detail.wrapped if lubrication_detail else None, new_name if new_name else None)
        return method_result

    def remove(self, lubrication_detail: '_259.LubricationDetail'):
        ''' 'Remove' is the original name of this method.

        Args:
            lubrication_detail (mastapy.materials.LubricationDetail)
        '''

        self.wrapped.Remove(lubrication_detail.wrapped if lubrication_detail else None)

    def get_all_items(self) -> 'Iterable[_259.LubricationDetail]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.materials.LubricationDetail]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_259.LubricationDetail))

    def save_changes(self, lubrication_detail: '_259.LubricationDetail'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            lubrication_detail (mastapy.materials.LubricationDetail)
        '''

        self.wrapped.SaveChanges(lubrication_detail.wrapped if lubrication_detail else None)
