'''_826.py

PinionConvex
'''


from mastapy.gears.manufacturing.bevel import (
    _827, _822, _823, _825,
    _828, _829, _830
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _844
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PINION_CONVEX = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionConvex')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionConvex',)


class PinionConvex(_1.APIBase):
    '''PinionConvex

    This is a mastapy class.
    '''

    TYPE = _PINION_CONVEX
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionConvex.TYPE'):
        super().__init__(instance_to_wrap)

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
    def pinion_convex_ib_configuration(self) -> '_844.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'PinionConvexIBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_844.BasicConicalGearMachineSettingsGenerated)(self.wrapped.PinionConvexIBConfiguration) if self.wrapped.PinionConvexIBConfiguration else None
