'''_815.py

ConicalWheelManufacturingConfig
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.cutters import _837, _836
from mastapy.gears.manufacturing.bevel.basic_machine_settings import (
    _846, _842, _843, _844
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import _797

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CONICAL_WHEEL_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalWheelManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalWheelManufacturingConfig',)


class ConicalWheelManufacturingConfig(_797.ConicalGearManufacturingConfig):
    '''ConicalWheelManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_WHEEL_MANUFACTURING_CONFIG
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalWheelManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_cutter_tilt(self) -> 'bool':
        '''bool: 'UseCutterTilt' is the original name of this property.'''

        return self.wrapped.UseCutterTilt

    @use_cutter_tilt.setter
    def use_cutter_tilt(self, value: 'bool'):
        self.wrapped.UseCutterTilt = bool(value) if value else False

    @property
    def wheel_finish_manufacturing_machine(self) -> 'str':
        '''str: 'WheelFinishManufacturingMachine' is the original name of this property.'''

        return self.wrapped.WheelFinishManufacturingMachine.SelectedItemName

    @wheel_finish_manufacturing_machine.setter
    def wheel_finish_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelFinishManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def wheel_rough_manufacturing_machine(self) -> 'str':
        '''str: 'WheelRoughManufacturingMachine' is the original name of this property.'''

        return self.wrapped.WheelRoughManufacturingMachine.SelectedItemName

    @wheel_rough_manufacturing_machine.setter
    def wheel_rough_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelRoughManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def wheel_rough_cutter(self) -> '_837.WheelRoughCutter':
        '''WheelRoughCutter: 'WheelRoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_837.WheelRoughCutter)(self.wrapped.WheelRoughCutter) if self.wrapped.WheelRoughCutter else None

    @property
    def wheel_finish_cutter(self) -> '_836.WheelFinishCutter':
        '''WheelFinishCutter: 'WheelFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_836.WheelFinishCutter)(self.wrapped.WheelFinishCutter) if self.wrapped.WheelFinishCutter else None

    @property
    def specified_cradle_style_machine_settings(self) -> '_846.CradleStyleConicalMachineSettingsGenerated':
        '''CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_846.CradleStyleConicalMachineSettingsGenerated)(self.wrapped.SpecifiedCradleStyleMachineSettings) if self.wrapped.SpecifiedCradleStyleMachineSettings else None

    @property
    def specified_machine_settings(self) -> '_842.BasicConicalGearMachineSettings':
        '''BasicConicalGearMachineSettings: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_842.BasicConicalGearMachineSettings)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_formate(self) -> '_843.BasicConicalGearMachineSettingsFormate':
        '''BasicConicalGearMachineSettingsFormate: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SpecifiedMachineSettings.__class__.__qualname__ != 'BasicConicalGearMachineSettingsFormate':
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsFormate. Expected: {}.'.format(self.wrapped.SpecifiedMachineSettings.__class__.__qualname__))

        return constructor.new(_843.BasicConicalGearMachineSettingsFormate)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_generated(self) -> '_844.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SpecifiedMachineSettings.__class__.__qualname__ != 'BasicConicalGearMachineSettingsGenerated':
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsGenerated. Expected: {}.'.format(self.wrapped.SpecifiedMachineSettings.__class__.__qualname__))

        return constructor.new(_844.BasicConicalGearMachineSettingsGenerated)(self.wrapped.SpecifiedMachineSettings) if self.wrapped.SpecifiedMachineSettings else None
