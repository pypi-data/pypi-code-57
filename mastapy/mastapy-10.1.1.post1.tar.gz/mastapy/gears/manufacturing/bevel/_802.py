'''_802.py

ConicalMeshFlankManufacturingConfig
'''


from mastapy.gears.manufacturing.bevel.control_parameters import (
    _838, _839, _840, _841
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _844, _846
from mastapy.gears.manufacturing.bevel import _803
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_FLANK_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshFlankManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshFlankManufacturingConfig',)


class ConicalMeshFlankManufacturingConfig(_803.ConicalMeshFlankMicroGeometryConfig):
    '''ConicalMeshFlankManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_FLANK_MANUFACTURING_CONFIG
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshFlankManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def control_parameters(self) -> '_838.ConicalGearManufacturingControlParameters':
        '''ConicalGearManufacturingControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_838.ConicalGearManufacturingControlParameters)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgm_control_parameters(self) -> '_839.ConicalManufacturingSGMControlParameters':
        '''ConicalManufacturingSGMControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ControlParameters.__class__.__qualname__ != 'ConicalManufacturingSGMControlParameters':
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGMControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new(_839.ConicalManufacturingSGMControlParameters)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgt_control_parameters(self) -> '_840.ConicalManufacturingSGTControlParameters':
        '''ConicalManufacturingSGTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ControlParameters.__class__.__qualname__ != 'ConicalManufacturingSGTControlParameters':
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGTControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new(_840.ConicalManufacturingSGTControlParameters)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_smt_control_parameters(self) -> '_841.ConicalManufacturingSMTControlParameters':
        '''ConicalManufacturingSMTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ControlParameters.__class__.__qualname__ != 'ConicalManufacturingSMTControlParameters':
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSMTControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new(_841.ConicalManufacturingSMTControlParameters)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def specified_phoenix_style_machine_settings(self) -> '_844.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'SpecifiedPhoenixStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_844.BasicConicalGearMachineSettingsGenerated)(self.wrapped.SpecifiedPhoenixStyleMachineSettings) if self.wrapped.SpecifiedPhoenixStyleMachineSettings else None

    @property
    def specified_cradle_style_machine_settings(self) -> '_846.CradleStyleConicalMachineSettingsGenerated':
        '''CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_846.CradleStyleConicalMachineSettingsGenerated)(self.wrapped.SpecifiedCradleStyleMachineSettings) if self.wrapped.SpecifiedCradleStyleMachineSettings else None
