'''_6235.py

ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_SINGLE_DEGREE_OF_FREEDOM_OF_RESPONSE_OF_NODE_IN_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic',)


TYMeasurement = TypeVar('TYMeasurement', bound='_1035.MeasurementBase')
TIntegralMeasurement = TypeVar('TIntegralMeasurement', bound='_1035.MeasurementBase')


class ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic(_1.APIBase, Generic[TYMeasurement, TIntegralMeasurement]):
    '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

    This is a mastapy class.

    Generic Types:
        TYMeasurement
        TIntegralMeasurement
    '''

    TYPE = _RESULTS_FOR_SINGLE_DEGREE_OF_FREEDOM_OF_RESPONSE_OF_NODE_IN_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def max(self) -> 'float':
        '''float: 'Max' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Max

    @property
    def frequency_of_max(self) -> 'float':
        '''float: 'FrequencyOfMax' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FrequencyOfMax

    @property
    def integral(self) -> 'float':
        '''float: 'Integral' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Integral
