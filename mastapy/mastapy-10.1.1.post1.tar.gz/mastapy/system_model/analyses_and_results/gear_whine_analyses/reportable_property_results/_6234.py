'''_6234.py

ResultsForResponseOfANodeOnAHarmonic
'''


from typing import List, Generic, TypeVar

from mastapy.system_model.analyses_and_results.gear_whine_analyses.reportable_property_results import _6235, _6225
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'ResultsForResponseOfANodeOnAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForResponseOfANodeOnAHarmonic',)


TLinearMeasurement = TypeVar('TLinearMeasurement', bound='_1035.MeasurementBase')
TLinearDerivativeMeasurement = TypeVar('TLinearDerivativeMeasurement', bound='_1035.MeasurementBase')
TAngularMeasurement = TypeVar('TAngularMeasurement', bound='_1035.MeasurementBase')
TAngularDerivativeMeasurement = TypeVar('TAngularDerivativeMeasurement', bound='_1035.MeasurementBase')


class ResultsForResponseOfANodeOnAHarmonic(_1.APIBase, Generic[TLinearMeasurement, TLinearDerivativeMeasurement, TAngularMeasurement, TAngularDerivativeMeasurement]):
    '''ResultsForResponseOfANodeOnAHarmonic

    This is a mastapy class.

    Generic Types:
        TLinearMeasurement
        TLinearDerivativeMeasurement
        TAngularMeasurement
        TAngularDerivativeMeasurement
    '''

    TYPE = _RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultsForResponseOfANodeOnAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def x(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]: 'X' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TLinearMeasurement, TLinearDerivativeMeasurement](self.wrapped.X) if self.wrapped.X else None

    @property
    def y(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TLinearMeasurement, TLinearDerivativeMeasurement](self.wrapped.Y) if self.wrapped.Y else None

    @property
    def z(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TLinearMeasurement, TLinearDerivativeMeasurement](self.wrapped.Z) if self.wrapped.Z else None

    @property
    def linear_magnitude(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]: 'LinearMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TLinearMeasurement, TLinearDerivativeMeasurement](self.wrapped.LinearMagnitude) if self.wrapped.LinearMagnitude else None

    @property
    def radial_magnitude(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TLinearMeasurement, TLinearDerivativeMeasurement]: 'RadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TLinearMeasurement, TLinearDerivativeMeasurement](self.wrapped.RadialMagnitude) if self.wrapped.RadialMagnitude else None

    @property
    def theta_x(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]: 'ThetaX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TAngularMeasurement, TAngularDerivativeMeasurement](self.wrapped.ThetaX) if self.wrapped.ThetaX else None

    @property
    def theta_y(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]: 'ThetaY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TAngularMeasurement, TAngularDerivativeMeasurement](self.wrapped.ThetaY) if self.wrapped.ThetaY else None

    @property
    def theta_z(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]: 'ThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TAngularMeasurement, TAngularDerivativeMeasurement](self.wrapped.ThetaZ) if self.wrapped.ThetaZ else None

    @property
    def angular_magnitude(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]: 'AngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TAngularMeasurement, TAngularDerivativeMeasurement](self.wrapped.AngularMagnitude) if self.wrapped.AngularMagnitude else None

    @property
    def radial_angular_magnitude(self) -> '_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic[TAngularMeasurement, TAngularDerivativeMeasurement]: 'RadialAngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)[TAngularMeasurement, TAngularDerivativeMeasurement](self.wrapped.RadialAngularMagnitude) if self.wrapped.RadialAngularMagnitude else None

    @property
    def data_points(self) -> 'List[_6225.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic[TLinearMeasurement, TAngularMeasurement]]':
        '''List[DatapointForResponseOfANodeAtAFrequencyOnAHarmonic[TLinearMeasurement, TAngularMeasurement]]: 'DataPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DataPoints, constructor.new(_6225.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic)[TLinearMeasurement, TAngularMeasurement])
        return value
