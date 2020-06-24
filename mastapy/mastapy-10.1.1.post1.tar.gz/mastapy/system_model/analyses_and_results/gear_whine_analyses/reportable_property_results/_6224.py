'''_6224.py

DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_DATAPOINT_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_AT_A_FREQUENCY_IN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic',)


TLinearMeasurement = TypeVar('TLinearMeasurement', bound='_1035.MeasurementBase')


class DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic(_1.APIBase, Generic[TLinearMeasurement]):
    '''DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic

    This is a mastapy class.

    Generic Types:
        TLinearMeasurement
    '''

    TYPE = _DATAPOINT_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_AT_A_FREQUENCY_IN_A_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def speed(self) -> 'float':
        '''float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Speed

    @property
    def frequency(self) -> 'float':
        '''float: 'Frequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Frequency

    @property
    def response(self) -> 'complex':
        '''complex: 'Response' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_complex(self.wrapped.Response)
        return constructor.new(complex)(value) if value else None
