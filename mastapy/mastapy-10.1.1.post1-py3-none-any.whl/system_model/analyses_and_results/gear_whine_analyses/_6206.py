'''_6206.py

GearWhineAnalysisOptions
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.system_model.analyses_and_results.modal_analyses import _5888
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _6185, _6184
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearWhineAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisOptions',)


class GearWhineAnalysisOptions(_1.APIBase):
    '''GearWhineAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def amplitude_cut_off_for_linear_te(self) -> 'float':
        '''float: 'AmplitudeCutOffForLinearTE' is the original name of this property.'''

        return self.wrapped.AmplitudeCutOffForLinearTE

    @amplitude_cut_off_for_linear_te.setter
    def amplitude_cut_off_for_linear_te(self, value: 'float'):
        self.wrapped.AmplitudeCutOffForLinearTE = float(value) if value else 0.0

    @property
    def amplitude_cut_off_for_misalignment_excitation(self) -> 'float':
        '''float: 'AmplitudeCutOffForMisalignmentExcitation' is the original name of this property.'''

        return self.wrapped.AmplitudeCutOffForMisalignmentExcitation

    @amplitude_cut_off_for_misalignment_excitation.setter
    def amplitude_cut_off_for_misalignment_excitation(self, value: 'float'):
        self.wrapped.AmplitudeCutOffForMisalignmentExcitation = float(value) if value else 0.0

    @property
    def modal_damping_factor(self) -> 'float':
        '''float: 'ModalDampingFactor' is the original name of this property.'''

        return self.wrapped.ModalDampingFactor

    @modal_damping_factor.setter
    def modal_damping_factor(self, value: 'float'):
        self.wrapped.ModalDampingFactor = float(value) if value else 0.0

    @property
    def rayleigh_damping_alpha(self) -> 'float':
        '''float: 'RayleighDampingAlpha' is the original name of this property.'''

        return self.wrapped.RayleighDampingAlpha

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'float'):
        self.wrapped.RayleighDampingAlpha = float(value) if value else 0.0

    @property
    def rayleigh_damping_beta(self) -> 'float':
        '''float: 'RayleighDampingBeta' is the original name of this property.'''

        return self.wrapped.RayleighDampingBeta

    @rayleigh_damping_beta.setter
    def rayleigh_damping_beta(self, value: 'float'):
        self.wrapped.RayleighDampingBeta = float(value) if value else 0.0

    @property
    def specify_per_mode_damping_factors(self) -> 'bool':
        '''bool: 'SpecifyPerModeDampingFactors' is the original name of this property.'''

        return self.wrapped.SpecifyPerModeDampingFactors

    @specify_per_mode_damping_factors.setter
    def specify_per_mode_damping_factors(self, value: 'bool'):
        self.wrapped.SpecifyPerModeDampingFactors = bool(value) if value else False

    @property
    def remove_last_point_from_advanced_system_deflection_te_for_fft_for_advanced_system_deflection_current_load_case_set_up(self) -> 'bool':
        '''bool: 'RemoveLastPointFromAdvancedSystemDeflectionTEForFFTForAdvancedSystemDeflectionCurrentLoadCaseSetUp' is the original name of this property.'''

        return self.wrapped.RemoveLastPointFromAdvancedSystemDeflectionTEForFFTForAdvancedSystemDeflectionCurrentLoadCaseSetUp

    @remove_last_point_from_advanced_system_deflection_te_for_fft_for_advanced_system_deflection_current_load_case_set_up.setter
    def remove_last_point_from_advanced_system_deflection_te_for_fft_for_advanced_system_deflection_current_load_case_set_up(self, value: 'bool'):
        self.wrapped.RemoveLastPointFromAdvancedSystemDeflectionTEForFFTForAdvancedSystemDeflectionCurrentLoadCaseSetUp = bool(value) if value else False

    @property
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(self) -> 'bool':
        '''bool: 'UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions' is the original name of this property.'''

        return self.wrapped.UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions

    @use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options.setter
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(self, value: 'bool'):
        self.wrapped.UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions = bool(value) if value else False

    @property
    def include_misalignment_excitation(self) -> 'bool':
        '''bool: 'IncludeMisalignmentExcitation' is the original name of this property.'''

        return self.wrapped.IncludeMisalignmentExcitation

    @include_misalignment_excitation.setter
    def include_misalignment_excitation(self, value: 'bool'):
        self.wrapped.IncludeMisalignmentExcitation = bool(value) if value else False

    @property
    def number_of_harmonics(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfHarmonics' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfHarmonics) if self.wrapped.NumberOfHarmonics else None

    @number_of_harmonics.setter
    def number_of_harmonics(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfHarmonics = value

    @property
    def crop_to_speed_range_for_export_and_reports(self) -> 'bool':
        '''bool: 'CropToSpeedRangeForExportAndReports' is the original name of this property.'''

        return self.wrapped.CropToSpeedRangeForExportAndReports

    @crop_to_speed_range_for_export_and_reports.setter
    def crop_to_speed_range_for_export_and_reports(self, value: 'bool'):
        self.wrapped.CropToSpeedRangeForExportAndReports = bool(value) if value else False

    @property
    def penalty_mass_for_enforced_te(self) -> 'float':
        '''float: 'PenaltyMassForEnforcedTE' is the original name of this property.'''

        return self.wrapped.PenaltyMassForEnforcedTE

    @penalty_mass_for_enforced_te.setter
    def penalty_mass_for_enforced_te(self, value: 'float'):
        self.wrapped.PenaltyMassForEnforcedTE = float(value) if value else 0.0

    @property
    def modal_analysis_options(self) -> '_5888.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'ModalAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5888.ModalAnalysisOptions)(self.wrapped.ModalAnalysisOptions) if self.wrapped.ModalAnalysisOptions else None

    @property
    def reference_speed_options(self) -> '_6185.SpeedOptionsForGearWhineAnalysisResults':
        '''SpeedOptionsForGearWhineAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.SpeedOptionsForGearWhineAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def frequency_options(self) -> '_6184.FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def per_mode_damping_factors(self) -> 'List[float]':
        '''List[float]: 'PerModeDampingFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PerModeDampingFactors, float)
        return value

    def set_per_mode_damping_factors(self, damping_values: 'List[float]'):
        ''' 'SetPerModeDampingFactors' is the original name of this method.

        Args:
            damping_values (List[float])
        '''

        damping_values = conversion.mp_to_pn_objects_in_list(damping_values)
        self.wrapped.SetPerModeDampingFactors(damping_values)

    def set_per_mode_damping_factor(self, mode: 'int', damping: 'float'):
        ''' 'SetPerModeDampingFactor' is the original name of this method.

        Args:
            mode (int)
            damping (float)
        '''

        mode = int(mode)
        damping = float(damping)
        self.wrapped.SetPerModeDampingFactor(mode if mode else 0, damping if damping else 0.0)
