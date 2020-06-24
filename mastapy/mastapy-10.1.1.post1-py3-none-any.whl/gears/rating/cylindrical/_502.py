'''_502.py

ScuffingResultsRow
'''


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical import _503
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SCUFFING_RESULTS_ROW = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'ScuffingResultsRow')


__docformat__ = 'restructuredtext en'
__all__ = ('ScuffingResultsRow',)


class ScuffingResultsRow(_1.APIBase):
    '''ScuffingResultsRow

    This is a mastapy class.
    '''

    TYPE = _SCUFFING_RESULTS_ROW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ScuffingResultsRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flash_temperature(self) -> 'float':
        '''float: 'FlashTemperature' is the original name of this property.'''

        return self.wrapped.FlashTemperature

    @flash_temperature.setter
    def flash_temperature(self, value: 'float'):
        self.wrapped.FlashTemperature = float(value) if value else 0.0

    @property
    def contact_temperature(self) -> 'float':
        '''float: 'ContactTemperature' is the original name of this property.'''

        return self.wrapped.ContactTemperature

    @contact_temperature.setter
    def contact_temperature(self, value: 'float'):
        self.wrapped.ContactTemperature = float(value) if value else 0.0

    @property
    def index_label(self) -> 'str':
        '''str: 'IndexLabel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IndexLabel

    @property
    def pinion_flank_transverse_radius_of_curvature(self) -> 'float':
        '''float: 'PinionFlankTransverseRadiusOfCurvature' is the original name of this property.'''

        return self.wrapped.PinionFlankTransverseRadiusOfCurvature

    @pinion_flank_transverse_radius_of_curvature.setter
    def pinion_flank_transverse_radius_of_curvature(self, value: 'float'):
        self.wrapped.PinionFlankTransverseRadiusOfCurvature = float(value) if value else 0.0

    @property
    def wheel_flank_transverse_radius_of_curvature(self) -> 'float':
        '''float: 'WheelFlankTransverseRadiusOfCurvature' is the original name of this property.'''

        return self.wrapped.WheelFlankTransverseRadiusOfCurvature

    @wheel_flank_transverse_radius_of_curvature.setter
    def wheel_flank_transverse_radius_of_curvature(self, value: 'float'):
        self.wrapped.WheelFlankTransverseRadiusOfCurvature = float(value) if value else 0.0

    @property
    def load_sharing_factor(self) -> 'float':
        '''float: 'LoadSharingFactor' is the original name of this property.'''

        return self.wrapped.LoadSharingFactor

    @load_sharing_factor.setter
    def load_sharing_factor(self, value: 'float'):
        self.wrapped.LoadSharingFactor = float(value) if value else 0.0

    @property
    def normal_relative_radius_of_curvature(self) -> 'float':
        '''float: 'NormalRelativeRadiusOfCurvature' is the original name of this property.'''

        return self.wrapped.NormalRelativeRadiusOfCurvature

    @normal_relative_radius_of_curvature.setter
    def normal_relative_radius_of_curvature(self, value: 'float'):
        self.wrapped.NormalRelativeRadiusOfCurvature = float(value) if value else 0.0

    @property
    def line_of_action_parameter(self) -> 'float':
        '''float: 'LineOfActionParameter' is the original name of this property.'''

        return self.wrapped.LineOfActionParameter

    @line_of_action_parameter.setter
    def line_of_action_parameter(self, value: 'float'):
        self.wrapped.LineOfActionParameter = float(value) if value else 0.0

    @property
    def pinion(self) -> '_503.ScuffingResultsRowGear':
        '''ScuffingResultsRowGear: 'Pinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_503.ScuffingResultsRowGear)(self.wrapped.Pinion) if self.wrapped.Pinion else None
