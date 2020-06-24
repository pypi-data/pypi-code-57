'''_809.py

ConicalPinionManufacturingConfig
'''


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel import (
    _806, _802, _827, _822,
    _823, _825, _828, _829,
    _830, _831, _797
)
from mastapy.gears.manufacturing.bevel.cutters import _834, _835
from mastapy._internal.cast_exception import CastException

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CONICAL_PINION_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalPinionManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalPinionManufacturingConfig',)


class ConicalPinionManufacturingConfig(_797.ConicalGearManufacturingConfig):
    '''ConicalPinionManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_PINION_MANUFACTURING_CONFIG
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalPinionManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pinion_finish_manufacturing_machine(self) -> 'str':
        '''str: 'PinionFinishManufacturingMachine' is the original name of this property.'''

        return self.wrapped.PinionFinishManufacturingMachine.SelectedItemName

    @pinion_finish_manufacturing_machine.setter
    def pinion_finish_manufacturing_machine(self, value: 'str'):
        self.wrapped.PinionFinishManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def pinion_rough_manufacturing_machine(self) -> 'str':
        '''str: 'PinionRoughManufacturingMachine' is the original name of this property.'''

        return self.wrapped.PinionRoughManufacturingMachine.SelectedItemName

    @pinion_rough_manufacturing_machine.setter
    def pinion_rough_manufacturing_machine(self, value: 'str'):
        self.wrapped.PinionRoughManufacturingMachine.SetSelectedItem(str(value) if value else None)

    @property
    def mesh_config(self) -> '_806.ConicalMeshManufacturingConfig':
        '''ConicalMeshManufacturingConfig: 'MeshConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_806.ConicalMeshManufacturingConfig)(self.wrapped.MeshConfig) if self.wrapped.MeshConfig else None

    @property
    def pinion_concave_ob_configuration(self) -> '_802.ConicalMeshFlankManufacturingConfig':
        '''ConicalMeshFlankManufacturingConfig: 'PinionConcaveOBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_802.ConicalMeshFlankManufacturingConfig)(self.wrapped.PinionConcaveOBConfiguration) if self.wrapped.PinionConcaveOBConfiguration else None

    @property
    def pinion_convex_ib_configuration(self) -> '_802.ConicalMeshFlankManufacturingConfig':
        '''ConicalMeshFlankManufacturingConfig: 'PinionConvexIBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_802.ConicalMeshFlankManufacturingConfig)(self.wrapped.PinionConvexIBConfiguration) if self.wrapped.PinionConvexIBConfiguration else None

    @property
    def pinion_finish_cutter(self) -> '_834.PinionFinishCutter':
        '''PinionFinishCutter: 'PinionFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_834.PinionFinishCutter)(self.wrapped.PinionFinishCutter) if self.wrapped.PinionFinishCutter else None

    @property
    def pinion_rough_cutter(self) -> '_835.PinionRoughCutter':
        '''PinionRoughCutter: 'PinionRoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_835.PinionRoughCutter)(self.wrapped.PinionRoughCutter) if self.wrapped.PinionRoughCutter else None

    @property
    def pinion_cutter_parameters_concave(self) -> '_827.PinionFinishMachineSettings':
        '''PinionFinishMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_827.PinionFinishMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_modified_roll_machine_settings(self) -> '_822.PinionBevelGeneratingModifiedRollMachineSettings':
        '''PinionBevelGeneratingModifiedRollMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionBevelGeneratingModifiedRollMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingModifiedRollMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_822.PinionBevelGeneratingModifiedRollMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_tilt_machine_settings(self) -> '_823.PinionBevelGeneratingTiltMachineSettings':
        '''PinionBevelGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionBevelGeneratingTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_823.PinionBevelGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_conical_machine_settings_specified(self) -> '_825.PinionConicalMachineSettingsSpecified':
        '''PinionConicalMachineSettingsSpecified: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionConicalMachineSettingsSpecified':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionConicalMachineSettingsSpecified. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_825.PinionConicalMachineSettingsSpecified)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_formate_tilt_machine_settings(self) -> '_828.PinionHypoidFormateTiltMachineSettings':
        '''PinionHypoidFormateTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionHypoidFormateTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidFormateTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_828.PinionHypoidFormateTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_generating_tilt_machine_settings(self) -> '_829.PinionHypoidGeneratingTiltMachineSettings':
        '''PinionHypoidGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionHypoidGeneratingTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_829.PinionHypoidGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_machine_settings_smt(self) -> '_830.PinionMachineSettingsSMT':
        '''PinionMachineSettingsSMT: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConcave.__class__.__qualname__ != 'PinionMachineSettingsSMT':
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionMachineSettingsSMT. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_830.PinionMachineSettingsSMT)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_convex(self) -> '_827.PinionFinishMachineSettings':
        '''PinionFinishMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_827.PinionFinishMachineSettings)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_bevel_generating_modified_roll_machine_settings(self) -> '_822.PinionBevelGeneratingModifiedRollMachineSettings':
        '''PinionBevelGeneratingModifiedRollMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionBevelGeneratingModifiedRollMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionBevelGeneratingModifiedRollMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_822.PinionBevelGeneratingModifiedRollMachineSettings)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_bevel_generating_tilt_machine_settings(self) -> '_823.PinionBevelGeneratingTiltMachineSettings':
        '''PinionBevelGeneratingTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionBevelGeneratingTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionBevelGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_823.PinionBevelGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_conical_machine_settings_specified(self) -> '_825.PinionConicalMachineSettingsSpecified':
        '''PinionConicalMachineSettingsSpecified: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionConicalMachineSettingsSpecified':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionConicalMachineSettingsSpecified. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_825.PinionConicalMachineSettingsSpecified)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_hypoid_formate_tilt_machine_settings(self) -> '_828.PinionHypoidFormateTiltMachineSettings':
        '''PinionHypoidFormateTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionHypoidFormateTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionHypoidFormateTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_828.PinionHypoidFormateTiltMachineSettings)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_hypoid_generating_tilt_machine_settings(self) -> '_829.PinionHypoidGeneratingTiltMachineSettings':
        '''PinionHypoidGeneratingTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionHypoidGeneratingTiltMachineSettings':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionHypoidGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_829.PinionHypoidGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_machine_settings_smt(self) -> '_830.PinionMachineSettingsSMT':
        '''PinionMachineSettingsSMT: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.PinionCutterParametersConvex.__class__.__qualname__ != 'PinionMachineSettingsSMT':
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionMachineSettingsSMT. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new(_830.PinionMachineSettingsSMT)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_rough_machine_setting(self) -> '_831.PinionRoughMachineSetting':
        '''PinionRoughMachineSetting: 'PinionRoughMachineSetting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_831.PinionRoughMachineSetting)(self.wrapped.PinionRoughMachineSetting) if self.wrapped.PinionRoughMachineSetting else None
