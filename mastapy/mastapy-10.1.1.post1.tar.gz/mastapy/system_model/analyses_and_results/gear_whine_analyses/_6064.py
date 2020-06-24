'''_6064.py

FrequencyOptionsForGearWhineAnalysisResults
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _3853
from mastapy.system_model.analyses_and_results.static_loads import _2057
from mastapy._internal.python_net import python_net_import

_FREQUENCY_OPTIONS_FOR_GEAR_WHINE_ANALYSIS_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'FrequencyOptionsForGearWhineAnalysisResults')


__docformat__ = 'restructuredtext en'
__all__ = ('FrequencyOptionsForGearWhineAnalysisResults',)


class FrequencyOptionsForGearWhineAnalysisResults(_3853.AbstractAnalysisOptions['_2057.StaticLoadCase']):
    '''FrequencyOptionsForGearWhineAnalysisResults

    This is a mastapy class.
    '''

    TYPE = _FREQUENCY_OPTIONS_FOR_GEAR_WHINE_ANALYSIS_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FrequencyOptionsForGearWhineAnalysisResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def minimum(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Minimum' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Minimum) if self.wrapped.Minimum else None

    @minimum.setter
    def minimum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Minimum = value

    @property
    def maximum(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Maximum' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Maximum) if self.wrapped.Maximum else None

    @maximum.setter
    def maximum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Maximum = value

    @property
    def create_data_points_at_mode_frequencies(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'CreateDataPointsAtModeFrequencies' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.CreateDataPointsAtModeFrequencies) if self.wrapped.CreateDataPointsAtModeFrequencies else None

    @create_data_points_at_mode_frequencies.setter
    def create_data_points_at_mode_frequencies(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.TYPE
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False)
        self.wrapped.CreateDataPointsAtModeFrequencies = value

    @property
    def additional_data_points_per_harmonic(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'AdditionalDataPointsPerHarmonic' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.AdditionalDataPointsPerHarmonic) if self.wrapped.AdditionalDataPointsPerHarmonic else None

    @additional_data_points_per_harmonic.setter
    def additional_data_points_per_harmonic(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.AdditionalDataPointsPerHarmonic = value

    @property
    def clustering_bias_of_additional_data_points(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ClusteringBiasOfAdditionalDataPoints' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ClusteringBiasOfAdditionalDataPoints) if self.wrapped.ClusteringBiasOfAdditionalDataPoints else None

    @clustering_bias_of_additional_data_points.setter
    def clustering_bias_of_additional_data_points(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ClusteringBiasOfAdditionalDataPoints = value

    @property
    def total_number_of_data_points_per_harmonic(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'TotalNumberOfDataPointsPerHarmonic' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.TotalNumberOfDataPointsPerHarmonic) if self.wrapped.TotalNumberOfDataPointsPerHarmonic else None

    @total_number_of_data_points_per_harmonic.setter
    def total_number_of_data_points_per_harmonic(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.TotalNumberOfDataPointsPerHarmonic = value

    @property
    def logarithmic_frequency_axis(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'LogarithmicFrequencyAxis' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.LogarithmicFrequencyAxis) if self.wrapped.LogarithmicFrequencyAxis else None

    @logarithmic_frequency_axis.setter
    def logarithmic_frequency_axis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.TYPE
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False)
        self.wrapped.LogarithmicFrequencyAxis = value

    @property
    def use_logarithmic_spacing_for_frequency_values(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'UseLogarithmicSpacingForFrequencyValues' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.UseLogarithmicSpacingForFrequencyValues) if self.wrapped.UseLogarithmicSpacingForFrequencyValues else None

    @use_logarithmic_spacing_for_frequency_values.setter
    def use_logarithmic_spacing_for_frequency_values(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.TYPE
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False)
        self.wrapped.UseLogarithmicSpacingForFrequencyValues = value

    @property
    def design_defaults(self) -> 'FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'DesignDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.DesignDefaults) if self.wrapped.DesignDefaults else None
