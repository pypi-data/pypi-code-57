'''_1192.py

BoltGeometryDatabase
'''


from typing import Iterable

from mastapy.bolts import _1191
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BOLT_GEOMETRY_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'BoltGeometryDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltGeometryDatabase',)


class BoltGeometryDatabase(_1.APIBase):
    '''BoltGeometryDatabase

    This is a mastapy class.
    '''

    TYPE = _BOLT_GEOMETRY_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltGeometryDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1191.BoltGeometry':
        '''BoltGeometry: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1191.BoltGeometry)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1191.BoltGeometry':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.bolts.BoltGeometry
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1191.BoltGeometry)(method_result) if method_result else None

    def can_be_removed(self, bolt_geometry: '_1191.BoltGeometry') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bolt_geometry (mastapy.bolts.BoltGeometry)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bolt_geometry.wrapped if bolt_geometry else None)
        return method_result

    def rename(self, bolt_geometry: '_1191.BoltGeometry', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bolt_geometry (mastapy.bolts.BoltGeometry)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bolt_geometry.wrapped if bolt_geometry else None, new_name if new_name else None)
        return method_result

    def remove(self, bolt_geometry: '_1191.BoltGeometry'):
        ''' 'Remove' is the original name of this method.

        Args:
            bolt_geometry (mastapy.bolts.BoltGeometry)
        '''

        self.wrapped.Remove(bolt_geometry.wrapped if bolt_geometry else None)

    def get_all_items(self) -> 'Iterable[_1191.BoltGeometry]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.bolts.BoltGeometry]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1191.BoltGeometry))

    def save_changes(self, bolt_geometry: '_1191.BoltGeometry'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bolt_geometry (mastapy.bolts.BoltGeometry)
        '''

        self.wrapped.SaveChanges(bolt_geometry.wrapped if bolt_geometry else None)
