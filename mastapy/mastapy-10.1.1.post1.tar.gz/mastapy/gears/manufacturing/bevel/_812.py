'''_812.py

ConicalSetManufacturingConfig
'''


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.gear_designs.conical import _947, _949
from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.bevel import _797, _806, _814
from mastapy._internal.python_net import python_net_import

_CONICAL_SET_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalSetManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalSetManufacturingConfig',)


class ConicalSetManufacturingConfig(_814.ConicalSetMicroGeometryConfigBase):
    '''ConicalSetManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_SET_MANUFACTURING_CONFIG
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalSetManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def manufacture_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods: 'ManufactureMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods)(self.wrapped.ManufactureMethod) if self.wrapped.ManufactureMethod else None

    @manufacture_method.setter
    def manufacture_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ManufactureMethod = value

    @property
    def machine_setting_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods: 'MachineSettingCalculationMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods)(self.wrapped.MachineSettingCalculationMethod) if self.wrapped.MachineSettingCalculationMethod else None

    @machine_setting_calculation_method.setter
    def machine_setting_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MachineSettingCalculationMethod = value

    @property
    def gear_manufacturing_configurations(self) -> 'List[_797.ConicalGearManufacturingConfig]':
        '''List[ConicalGearManufacturingConfig]: 'GearManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearManufacturingConfigurations, constructor.new(_797.ConicalGearManufacturingConfig))
        return value

    @property
    def meshes(self) -> 'List[_806.ConicalMeshManufacturingConfig]':
        '''List[ConicalMeshManufacturingConfig]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_806.ConicalMeshManufacturingConfig))
        return value
