'''_601.py

KlingelnbergConicalGearMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _602
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_GEAR_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'KlingelnbergConicalGearMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalGearMaterialDatabase',)


class KlingelnbergConicalGearMaterialDatabase(_1.APIBase):
    '''KlingelnbergConicalGearMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CONICAL_GEAR_MATERIAL_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalGearMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_602.KlingelnbergCycloPalloidConicalGearMaterial':
        '''KlingelnbergCycloPalloidConicalGearMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_602.KlingelnbergCycloPalloidConicalGearMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_602.KlingelnbergCycloPalloidConicalGearMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_602.KlingelnbergCycloPalloidConicalGearMaterial)(method_result) if method_result else None

    def can_be_removed(self, klingelnberg_cyclo_palloid_conical_gear_material: '_602.KlingelnbergCycloPalloidConicalGearMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            klingelnberg_cyclo_palloid_conical_gear_material (mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(klingelnberg_cyclo_palloid_conical_gear_material.wrapped if klingelnberg_cyclo_palloid_conical_gear_material else None)
        return method_result

    def rename(self, klingelnberg_cyclo_palloid_conical_gear_material: '_602.KlingelnbergCycloPalloidConicalGearMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            klingelnberg_cyclo_palloid_conical_gear_material (mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(klingelnberg_cyclo_palloid_conical_gear_material.wrapped if klingelnberg_cyclo_palloid_conical_gear_material else None, new_name if new_name else None)
        return method_result

    def remove(self, klingelnberg_cyclo_palloid_conical_gear_material: '_602.KlingelnbergCycloPalloidConicalGearMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            klingelnberg_cyclo_palloid_conical_gear_material (mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial)
        '''

        self.wrapped.Remove(klingelnberg_cyclo_palloid_conical_gear_material.wrapped if klingelnberg_cyclo_palloid_conical_gear_material else None)

    def get_all_items(self) -> 'Iterable[_602.KlingelnbergCycloPalloidConicalGearMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_602.KlingelnbergCycloPalloidConicalGearMaterial))

    def save_changes(self, klingelnberg_cyclo_palloid_conical_gear_material: '_602.KlingelnbergCycloPalloidConicalGearMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            klingelnberg_cyclo_palloid_conical_gear_material (mastapy.gears.materials.KlingelnbergCycloPalloidConicalGearMaterial)
        '''

        self.wrapped.SaveChanges(klingelnberg_cyclo_palloid_conical_gear_material.wrapped if klingelnberg_cyclo_palloid_conical_gear_material else None)
