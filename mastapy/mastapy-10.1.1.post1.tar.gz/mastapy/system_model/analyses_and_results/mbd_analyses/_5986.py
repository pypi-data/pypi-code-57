'''_5986.py

MBDRunUpAnalysisOptions
'''


from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5972, _6007, _6002
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.analysis_cases import _3380
from mastapy.system_model.analyses_and_results.static_loads import _5147
from mastapy._internal.python_net import python_net_import

_MBD_RUN_UP_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MBDRunUpAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MBDRunUpAnalysisOptions',)


class MBDRunUpAnalysisOptions(_3380.AbstractAnalysisOptions['_5147.TimeSeriesLoadCase']):
    '''MBDRunUpAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _MBD_RUN_UP_ANALYSIS_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MBDRunUpAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def time_to_reach_minimum_speed(self) -> 'float':
        '''float: 'TimeToReachMinimumSpeed' is the original name of this property.'''

        return self.wrapped.TimeToReachMinimumSpeed

    @time_to_reach_minimum_speed.setter
    def time_to_reach_minimum_speed(self, value: 'float'):
        self.wrapped.TimeToReachMinimumSpeed = float(value) if value else 0.0

    @property
    def time_to_keep_linear_speed_before_reaching_minimum_speed(self) -> 'float':
        '''float: 'TimeToKeepLinearSpeedBeforeReachingMinimumSpeed' is the original name of this property.'''

        return self.wrapped.TimeToKeepLinearSpeedBeforeReachingMinimumSpeed

    @time_to_keep_linear_speed_before_reaching_minimum_speed.setter
    def time_to_keep_linear_speed_before_reaching_minimum_speed(self, value: 'float'):
        self.wrapped.TimeToKeepLinearSpeedBeforeReachingMinimumSpeed = float(value) if value else 0.0

    @property
    def polynomial_order(self) -> 'int':
        '''int: 'PolynomialOrder' is the original name of this property.'''

        return self.wrapped.PolynomialOrder

    @polynomial_order.setter
    def polynomial_order(self, value: 'int'):
        self.wrapped.PolynomialOrder = int(value) if value else 0

    @property
    def input_velocity_processing_type(self) -> '_5972.InputVelocityForRunUpProcessingType':
        '''InputVelocityForRunUpProcessingType: 'InputVelocityProcessingType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.InputVelocityProcessingType)
        return constructor.new(_5972.InputVelocityForRunUpProcessingType)(value) if value else None

    @input_velocity_processing_type.setter
    def input_velocity_processing_type(self, value: '_5972.InputVelocityForRunUpProcessingType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InputVelocityProcessingType = value

    @property
    def power_load_for_run_up_torque(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'PowerLoadForRunUpTorque' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.PowerLoadForRunUpTorque) if self.wrapped.PowerLoadForRunUpTorque else None

    @power_load_for_run_up_torque.setter
    def power_load_for_run_up_torque(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.PowerLoadForRunUpTorque = value

    @property
    def shape_of_initial_acceleration_period(self) -> '_6007.ShapeOfInitialAccelerationPeriodForRunUp':
        '''ShapeOfInitialAccelerationPeriodForRunUp: 'ShapeOfInitialAccelerationPeriod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ShapeOfInitialAccelerationPeriod)
        return constructor.new(_6007.ShapeOfInitialAccelerationPeriodForRunUp)(value) if value else None

    @shape_of_initial_acceleration_period.setter
    def shape_of_initial_acceleration_period(self, value: '_6007.ShapeOfInitialAccelerationPeriodForRunUp'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ShapeOfInitialAccelerationPeriod = value

    @property
    def run_up_driving_mode(self) -> '_6002.RunUpDrivingMode':
        '''RunUpDrivingMode: 'RunUpDrivingMode' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RunUpDrivingMode)
        return constructor.new(_6002.RunUpDrivingMode)(value) if value else None

    @run_up_driving_mode.setter
    def run_up_driving_mode(self, value: '_6002.RunUpDrivingMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RunUpDrivingMode = value

    @property
    def run_up_start_speed(self) -> 'float':
        '''float: 'RunUpStartSpeed' is the original name of this property.'''

        return self.wrapped.RunUpStartSpeed

    @run_up_start_speed.setter
    def run_up_start_speed(self, value: 'float'):
        self.wrapped.RunUpStartSpeed = float(value) if value else 0.0

    @property
    def run_up_end_speed(self) -> 'float':
        '''float: 'RunUpEndSpeed' is the original name of this property.'''

        return self.wrapped.RunUpEndSpeed

    @run_up_end_speed.setter
    def run_up_end_speed(self, value: 'float'):
        self.wrapped.RunUpEndSpeed = float(value) if value else 0.0

    @property
    def reference_power_load_for_run_up_speed(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'ReferencePowerLoadForRunUpSpeed' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.ReferencePowerLoadForRunUpSpeed) if self.wrapped.ReferencePowerLoadForRunUpSpeed else None

    @reference_power_load_for_run_up_speed.setter
    def reference_power_load_for_run_up_speed(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.ReferencePowerLoadForRunUpSpeed = value
