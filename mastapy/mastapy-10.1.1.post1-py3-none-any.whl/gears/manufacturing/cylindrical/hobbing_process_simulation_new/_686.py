'''_686.py

ProcessCalculation
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _692, _673, _710
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessCalculation',)


class ProcessCalculation(_1.APIBase):
    '''ProcessCalculation

    This is a mastapy class.
    '''

    TYPE = _PROCESS_CALCULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessCalculation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def calculate_modifications(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateModifications

    @property
    def calculate_left_modifications(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateLeftModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateLeftModifications

    @property
    def calculate_right_modifications(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateRightModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateRightModifications

    @property
    def calculate_left_total_modifications(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateLeftTotalModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateLeftTotalModifications

    @property
    def calculate_right_total_modifications(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateRightTotalModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateRightTotalModifications

    @property
    def calculate_idle_distance(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateIdleDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateIdleDistance

    @property
    def calculate_maximum_shaft_mark_length(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateMaximumShaftMarkLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateMaximumShaftMarkLength

    @property
    def calculate_shaft_mark(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateShaftMark' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateShaftMark

    @property
    def shaft_mark_length(self) -> 'float':
        '''float: 'ShaftMarkLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftMarkLength

    @property
    def idle_distance(self) -> 'float':
        '''float: 'IdleDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IdleDistance

    @property
    def centre_distance_parabolic_parameter(self) -> 'float':
        '''float: 'CentreDistanceParabolicParameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistanceParabolicParameter

    @property
    def cutter_minimum_effective_length(self) -> 'float':
        '''float: 'CutterMinimumEffectiveLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterMinimumEffectiveLength

    @property
    def minimum_allowable_neck_width(self) -> 'float':
        '''float: 'MinimumAllowableNeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAllowableNeckWidth

    @property
    def neck_width(self) -> 'float':
        '''float: 'NeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NeckWidth

    @property
    def cutter_gear_rotation_ratio(self) -> 'float':
        '''float: 'CutterGearRotationRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterGearRotationRatio

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistance

    @property
    def shaft_angle(self) -> 'float':
        '''float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftAngle

    @property
    def setting_angle(self) -> 'float':
        '''float: 'SettingAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SettingAngle

    @property
    def inputs(self) -> '_692.ProcessSimulationInput':
        '''ProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_692.ProcessSimulationInput)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def inputs_of_type_hobbing_process_simulation_input(self) -> '_673.HobbingProcessSimulationInput':
        '''HobbingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Inputs.__class__.__qualname__ != 'HobbingProcessSimulationInput':
            raise CastException('Failed to cast inputs to HobbingProcessSimulationInput. Expected: {}.'.format(self.wrapped.Inputs.__class__.__qualname__))

        return constructor.new(_673.HobbingProcessSimulationInput)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def inputs_of_type_worm_grinding_process_simulation_input(self) -> '_710.WormGrindingProcessSimulationInput':
        '''WormGrindingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Inputs.__class__.__qualname__ != 'WormGrindingProcessSimulationInput':
            raise CastException('Failed to cast inputs to WormGrindingProcessSimulationInput. Expected: {}.'.format(self.wrapped.Inputs.__class__.__qualname__))

        return constructor.new(_710.WormGrindingProcessSimulationInput)(self.wrapped.Inputs) if self.wrapped.Inputs else None
