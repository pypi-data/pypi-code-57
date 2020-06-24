'''_832.py

Wheel
'''


from mastapy.gears.manufacturing.bevel.cutters import _836
from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _842, _843, _844
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_WHEEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'Wheel')


__docformat__ = 'restructuredtext en'
__all__ = ('Wheel',)


class Wheel(_1.APIBase):
    '''Wheel

    This is a mastapy class.
    '''

    TYPE = _WHEEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Wheel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def wheel_finish_cutter(self) -> '_836.WheelFinishCutter':
        '''WheelFinishCutter: 'WheelFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_836.WheelFinishCutter)(self.wrapped.WheelFinishCutter) if self.wrapped.WheelFinishCutter else None

    @property
    def basic_conical_gear_machine_settings(self) -> '_842.BasicConicalGearMachineSettings':
        '''BasicConicalGearMachineSettings: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_842.BasicConicalGearMachineSettings)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings else None

    @property
    def basic_conical_gear_machine_settings_of_type_basic_conical_gear_machine_settings_formate(self) -> '_843.BasicConicalGearMachineSettingsFormate':
        '''BasicConicalGearMachineSettingsFormate: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__ != 'BasicConicalGearMachineSettingsFormate':
            raise CastException('Failed to cast basic_conical_gear_machine_settings to BasicConicalGearMachineSettingsFormate. Expected: {}.'.format(self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__))

        return constructor.new(_843.BasicConicalGearMachineSettingsFormate)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings else None

    @property
    def basic_conical_gear_machine_settings_of_type_basic_conical_gear_machine_settings_generated(self) -> '_844.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__ != 'BasicConicalGearMachineSettingsGenerated':
            raise CastException('Failed to cast basic_conical_gear_machine_settings to BasicConicalGearMachineSettingsGenerated. Expected: {}.'.format(self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__))

        return constructor.new(_844.BasicConicalGearMachineSettingsGenerated)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings else None
