'''_1851.py

ElectricMachineDynamicLoadData
'''


from typing import List

from mastapy.system_model.imported_fes import _1850
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DYNAMIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ElectricMachineDynamicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDynamicLoadData',)


class ElectricMachineDynamicLoadData(_1.APIBase):
    '''ElectricMachineDynamicLoadData

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_DYNAMIC_LOAD_DATA
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineDynamicLoadData.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def electric_machine_data_sets(self) -> 'List[_1850.ElectricMachineDataSet]':
        '''List[ElectricMachineDataSet]: 'ElectricMachineDataSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElectricMachineDataSets, constructor.new(_1850.ElectricMachineDataSet))
        return value

    def add_electric_machine_data_set(self, name: 'str') -> '_1850.ElectricMachineDataSet':
        ''' 'AddElectricMachineDataSet' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.imported_fes.ElectricMachineDataSet
        '''

        name = str(name)
        method_result = self.wrapped.AddElectricMachineDataSet(name if name else None)
        return constructor.new(_1850.ElectricMachineDataSet)(method_result) if method_result else None
