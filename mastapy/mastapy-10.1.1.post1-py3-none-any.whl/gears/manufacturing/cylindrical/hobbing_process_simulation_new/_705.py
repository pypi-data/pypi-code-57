'''_705.py

RackManufactureError
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RACK_MANUFACTURE_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'RackManufactureError')


__docformat__ = 'restructuredtext en'
__all__ = ('RackManufactureError',)


class RackManufactureError(_1.APIBase):
    '''RackManufactureError

    This is a mastapy class.
    '''

    TYPE = _RACK_MANUFACTURE_ERROR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RackManufactureError.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def left_flank_pressure_angle_error_length(self) -> 'float':
        '''float: 'LeftFlankPressureAngleErrorLength' is the original name of this property.'''

        return self.wrapped.LeftFlankPressureAngleErrorLength

    @left_flank_pressure_angle_error_length.setter
    def left_flank_pressure_angle_error_length(self, value: 'float'):
        self.wrapped.LeftFlankPressureAngleErrorLength = float(value) if value else 0.0

    @property
    def right_flank_pressure_angle_error_length(self) -> 'float':
        '''float: 'RightFlankPressureAngleErrorLength' is the original name of this property.'''

        return self.wrapped.RightFlankPressureAngleErrorLength

    @right_flank_pressure_angle_error_length.setter
    def right_flank_pressure_angle_error_length(self, value: 'float'):
        self.wrapped.RightFlankPressureAngleErrorLength = float(value) if value else 0.0

    @property
    def left_flank_pressure_angle_error_reading(self) -> 'float':
        '''float: 'LeftFlankPressureAngleErrorReading' is the original name of this property.'''

        return self.wrapped.LeftFlankPressureAngleErrorReading

    @left_flank_pressure_angle_error_reading.setter
    def left_flank_pressure_angle_error_reading(self, value: 'float'):
        self.wrapped.LeftFlankPressureAngleErrorReading = float(value) if value else 0.0

    @property
    def right_flank_pressure_angle_error_reading(self) -> 'float':
        '''float: 'RightFlankPressureAngleErrorReading' is the original name of this property.'''

        return self.wrapped.RightFlankPressureAngleErrorReading

    @right_flank_pressure_angle_error_reading.setter
    def right_flank_pressure_angle_error_reading(self, value: 'float'):
        self.wrapped.RightFlankPressureAngleErrorReading = float(value) if value else 0.0
