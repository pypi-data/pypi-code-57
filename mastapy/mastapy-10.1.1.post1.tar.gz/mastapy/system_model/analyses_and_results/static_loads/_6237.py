'''_6237.py

HarmonicLoadDataBase
'''


from typing import Callable, List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.static_loads import _2061
from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1006
from mastapy.units_and_measurements import _2062
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_BASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataBase')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataBase',)


class HarmonicLoadDataBase(_1.APIBase):
    '''HarmonicLoadDataBase

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_LOAD_DATA_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def data_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType':
        '''enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType: 'DataType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType)(self.wrapped.DataType) if self.wrapped.DataType else None

    @data_type.setter
    def data_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DataType = value

    @property
    def clear_selected_data(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearSelectedData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearSelectedData

    @property
    def clear_all_data(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearAllData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearAllData

    @property
    def number_of_cycles_in_signal(self) -> 'float':
        '''float: 'NumberOfCyclesInSignal' is the original name of this property.'''

        return self.wrapped.NumberOfCyclesInSignal

    @number_of_cycles_in_signal.setter
    def number_of_cycles_in_signal(self, value: 'float'):
        self.wrapped.NumberOfCyclesInSignal = float(value) if value else 0.0

    @property
    def number_of_values(self) -> 'int':
        '''int: 'NumberOfValues' is the original name of this property.'''

        return self.wrapped.NumberOfValues

    @number_of_values.setter
    def number_of_values(self, value: 'int'):
        self.wrapped.NumberOfValues = int(value) if value else 0

    @property
    def number_of_harmonics(self) -> 'int':
        '''int: 'NumberOfHarmonics' is the original name of this property.'''

        return self.wrapped.NumberOfHarmonics

    @number_of_harmonics.setter
    def number_of_harmonics(self, value: 'int'):
        self.wrapped.NumberOfHarmonics = int(value) if value else 0

    @property
    def mean_value(self) -> 'float':
        '''float: 'MeanValue' is the original name of this property.'''

        return self.wrapped.MeanValue

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def peak_to_peak(self) -> 'float':
        '''float: 'PeakToPeak' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeak

    @property
    def excitations(self) -> 'List[_1006.FourierSeries]':
        '''List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Excitations, constructor.new(_1006.FourierSeries))
        return value

    def set_selected_harmonic_load_data(self, fourier_series_values: 'List[float]', fourier_series_name: 'str', fourier_series_measurement_type: '_2062.MeasurementType'):
        ''' 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        '''

        fourier_series_values = conversion.mp_to_pn_objects_in_list(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.SetSelectedHarmonicLoadData(fourier_series_values, fourier_series_name if fourier_series_name else None, fourier_series_measurement_type)

    def set_selected_harmonic_load_data_extended(self, amplitudes: 'List[float]', phases: 'List[float]', mean_value: 'float', fourier_series_name: 'str', fourier_series_measurement_type: '_2062.MeasurementType'):
        ''' 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            amplitudes (List[float])
            phases (List[float])
            mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        '''

        amplitudes = conversion.mp_to_pn_objects_in_list(amplitudes)
        phases = conversion.mp_to_pn_objects_in_list(phases)
        mean_value = float(mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.SetSelectedHarmonicLoadData(amplitudes, phases, mean_value if mean_value else 0.0, fourier_series_name if fourier_series_name else None, fourier_series_measurement_type)

    def set_selected_harmonic_load_data_with_fourier_series(self, fourier_series: '_1006.FourierSeries'):
        ''' 'SetSelectedHarmonicLoadData' is the original name of this method.

        Args:
            fourier_series (mastapy.math_utility.FourierSeries)
        '''

        self.wrapped.SetSelectedHarmonicLoadData(fourier_series.wrapped if fourier_series else None)
