'''_678.py

HobResharpeningError
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_HOB_RESHARPENING_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobResharpeningError')


__docformat__ = 'restructuredtext en'
__all__ = ('HobResharpeningError',)


class HobResharpeningError(_1.APIBase):
    '''HobResharpeningError

    This is a mastapy class.
    '''

    TYPE = _HOB_RESHARPENING_ERROR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobResharpeningError.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def radial_alignment_error_reading(self) -> 'float':
        '''float: 'RadialAlignmentErrorReading' is the original name of this property.'''

        return self.wrapped.RadialAlignmentErrorReading

    @radial_alignment_error_reading.setter
    def radial_alignment_error_reading(self, value: 'float'):
        self.wrapped.RadialAlignmentErrorReading = float(value) if value else 0.0

    @property
    def radial_alignment_measurement_length(self) -> 'float':
        '''float: 'RadialAlignmentMeasurementLength' is the original name of this property.'''

        return self.wrapped.RadialAlignmentMeasurementLength

    @radial_alignment_measurement_length.setter
    def radial_alignment_measurement_length(self, value: 'float'):
        self.wrapped.RadialAlignmentMeasurementLength = float(value) if value else 0.0

    @property
    def total_gash_indexing_variation(self) -> 'float':
        '''float: 'TotalGashIndexingVariation' is the original name of this property.'''

        return self.wrapped.TotalGashIndexingVariation

    @total_gash_indexing_variation.setter
    def total_gash_indexing_variation(self, value: 'float'):
        self.wrapped.TotalGashIndexingVariation = float(value) if value else 0.0

    @property
    def use_sin_curve_for_gash_index_variation(self) -> 'bool':
        '''bool: 'UseSinCurveForGashIndexVariation' is the original name of this property.'''

        return self.wrapped.UseSinCurveForGashIndexVariation

    @use_sin_curve_for_gash_index_variation.setter
    def use_sin_curve_for_gash_index_variation(self, value: 'bool'):
        self.wrapped.UseSinCurveForGashIndexVariation = bool(value) if value else False

    @property
    def gash_lead_error_reading(self) -> 'float':
        '''float: 'GashLeadErrorReading' is the original name of this property.'''

        return self.wrapped.GashLeadErrorReading

    @gash_lead_error_reading.setter
    def gash_lead_error_reading(self, value: 'float'):
        self.wrapped.GashLeadErrorReading = float(value) if value else 0.0

    @property
    def gash_lead_measurement_length(self) -> 'float':
        '''float: 'GashLeadMeasurementLength' is the original name of this property.'''

        return self.wrapped.GashLeadMeasurementLength

    @gash_lead_measurement_length.setter
    def gash_lead_measurement_length(self, value: 'float'):
        self.wrapped.GashLeadMeasurementLength = float(value) if value else 0.0
