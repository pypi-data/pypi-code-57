'''_1199.py

ClampedSectionMaterialDatabase
'''


from typing import Iterable

from mastapy.bolts import _1190
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CLAMPED_SECTION_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'ClampedSectionMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ClampedSectionMaterialDatabase',)


class ClampedSectionMaterialDatabase(_1.APIBase):
    '''ClampedSectionMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CLAMPED_SECTION_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClampedSectionMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1190.BoltedJointMaterial':
        '''BoltedJointMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1190.BoltedJointMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1190.BoltedJointMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.bolts.BoltedJointMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1190.BoltedJointMaterial)(method_result) if method_result else None

    def can_be_removed(self, bolted_joint_material: '_1190.BoltedJointMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bolted_joint_material (mastapy.bolts.BoltedJointMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bolted_joint_material.wrapped if bolted_joint_material else None)
        return method_result

    def rename(self, bolted_joint_material: '_1190.BoltedJointMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bolted_joint_material (mastapy.bolts.BoltedJointMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bolted_joint_material.wrapped if bolted_joint_material else None, new_name if new_name else None)
        return method_result

    def remove(self, bolted_joint_material: '_1190.BoltedJointMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            bolted_joint_material (mastapy.bolts.BoltedJointMaterial)
        '''

        self.wrapped.Remove(bolted_joint_material.wrapped if bolted_joint_material else None)

    def get_all_items(self) -> 'Iterable[_1190.BoltedJointMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.bolts.BoltedJointMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1190.BoltedJointMaterial))

    def save_changes(self, bolted_joint_material: '_1190.BoltedJointMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bolted_joint_material (mastapy.bolts.BoltedJointMaterial)
        '''

        self.wrapped.SaveChanges(bolted_joint_material.wrapped if bolted_joint_material else None)
