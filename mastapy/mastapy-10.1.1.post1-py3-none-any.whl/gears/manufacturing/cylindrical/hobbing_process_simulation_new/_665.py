'''_665.py

CutterHeadSlideError
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CUTTER_HEAD_SLIDE_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'CutterHeadSlideError')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterHeadSlideError',)


class CutterHeadSlideError(_1.APIBase):
    '''CutterHeadSlideError

    This is a mastapy class.
    '''

    TYPE = _CUTTER_HEAD_SLIDE_ERROR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CutterHeadSlideError.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def x_plane_measurement_length(self) -> 'float':
        '''float: 'XPlaneMeasurementLength' is the original name of this property.'''

        return self.wrapped.XPlaneMeasurementLength

    @x_plane_measurement_length.setter
    def x_plane_measurement_length(self, value: 'float'):
        self.wrapped.XPlaneMeasurementLength = float(value) if value else 0.0

    @property
    def y_plane_measurement_length(self) -> 'float':
        '''float: 'YPlaneMeasurementLength' is the original name of this property.'''

        return self.wrapped.YPlaneMeasurementLength

    @y_plane_measurement_length.setter
    def y_plane_measurement_length(self, value: 'float'):
        self.wrapped.YPlaneMeasurementLength = float(value) if value else 0.0

    @property
    def x_plane_measurement_reading(self) -> 'float':
        '''float: 'XPlaneMeasurementReading' is the original name of this property.'''

        return self.wrapped.XPlaneMeasurementReading

    @x_plane_measurement_reading.setter
    def x_plane_measurement_reading(self, value: 'float'):
        self.wrapped.XPlaneMeasurementReading = float(value) if value else 0.0

    @property
    def y_plane_measurement_reading(self) -> 'float':
        '''float: 'YPlaneMeasurementReading' is the original name of this property.'''

        return self.wrapped.YPlaneMeasurementReading

    @y_plane_measurement_reading.setter
    def y_plane_measurement_reading(self, value: 'float'):
        self.wrapped.YPlaneMeasurementReading = float(value) if value else 0.0
