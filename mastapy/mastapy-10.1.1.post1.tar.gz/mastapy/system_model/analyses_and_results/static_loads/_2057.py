'''_2057.py

StaticLoadCase
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.gears import _313
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6307
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _6206
from mastapy.system_model.analyses_and_results.load_case_groups import _6167, _6168
from mastapy.system_model.analyses_and_results.static_loads import _6181
from mastapy._internal.python_net import python_net_import

_STATIC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StaticLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticLoadCase',)


class StaticLoadCase(_6181.LoadCase):
    '''StaticLoadCase

    This is a mastapy class.
    '''

    TYPE = _STATIC_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StaticLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def design_state(self) -> 'str':
        '''str: 'DesignState' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignState

    @property
    def number_of_stop_start_cycles(self) -> 'int':
        '''int: 'NumberOfStopStartCycles' is the original name of this property.'''

        return self.wrapped.NumberOfStopStartCycles

    @number_of_stop_start_cycles.setter
    def number_of_stop_start_cycles(self, value: 'int'):
        self.wrapped.NumberOfStopStartCycles = int(value) if value else 0

    @property
    def is_stop_start_load_case(self) -> 'bool':
        '''bool: 'IsStopStartLoadCase' is the original name of this property.'''

        return self.wrapped.IsStopStartLoadCase

    @is_stop_start_load_case.setter
    def is_stop_start_load_case(self, value: 'bool'):
        self.wrapped.IsStopStartLoadCase = bool(value) if value else False

    @property
    def power_convergence_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PowerConvergenceTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PowerConvergenceTolerance) if self.wrapped.PowerConvergenceTolerance else None

    @power_convergence_tolerance.setter
    def power_convergence_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PowerConvergenceTolerance = value

    @property
    def run_power_flow(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RunPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RunPowerFlow

    @property
    def input_shaft_cycles(self) -> 'float':
        '''float: 'InputShaftCycles' is the original name of this property.'''

        return self.wrapped.InputShaftCycles

    @input_shaft_cycles.setter
    def input_shaft_cycles(self, value: 'float'):
        self.wrapped.InputShaftCycles = float(value) if value else 0.0

    @property
    def percentage_of_shaft_torque_alternating(self) -> 'float':
        '''float: 'PercentageOfShaftTorqueAlternating' is the original name of this property.'''

        return self.wrapped.PercentageOfShaftTorqueAlternating

    @percentage_of_shaft_torque_alternating.setter
    def percentage_of_shaft_torque_alternating(self, value: 'float'):
        self.wrapped.PercentageOfShaftTorqueAlternating = float(value) if value else 0.0

    @property
    def planetary_rating_load_sharing_method(self) -> '_313.PlanetaryRatingLoadSharingOption':
        '''PlanetaryRatingLoadSharingOption: 'PlanetaryRatingLoadSharingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryRatingLoadSharingMethod)
        return constructor.new(_313.PlanetaryRatingLoadSharingOption)(value) if value else None

    @planetary_rating_load_sharing_method.setter
    def planetary_rating_load_sharing_method(self, value: '_313.PlanetaryRatingLoadSharingOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryRatingLoadSharingMethod = value

    @property
    def current_time(self) -> 'float':
        '''float: 'CurrentTime' is the original name of this property.'''

        return self.wrapped.CurrentTime

    @current_time.setter
    def current_time(self, value: 'float'):
        self.wrapped.CurrentTime = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.'''

        return self.wrapped.Duration

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def set_face_widths_for_specified_safety_factors_from_power_flow(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow

    @property
    def create_time_series_load_case(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateTimeSeriesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateTimeSeriesLoadCase

    @property
    def advanced_system_deflection_options(self) -> '_6307.AdvancedSystemDeflectionOptions':
        '''AdvancedSystemDeflectionOptions: 'AdvancedSystemDeflectionOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6307.AdvancedSystemDeflectionOptions)(self.wrapped.AdvancedSystemDeflectionOptions) if self.wrapped.AdvancedSystemDeflectionOptions else None

    @property
    def gear_whine_harmonic_excitation_analysis_options(self) -> '_6206.GearWhineAnalysisOptions':
        '''GearWhineAnalysisOptions: 'GearWhineHarmonicExcitationAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6206.GearWhineAnalysisOptions)(self.wrapped.GearWhineHarmonicExcitationAnalysisOptions) if self.wrapped.GearWhineHarmonicExcitationAnalysisOptions else None

    @property
    def clutch_engagements(self) -> 'List[_6167.ClutchEngagementStatus]':
        '''List[ClutchEngagementStatus]: 'ClutchEngagements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClutchEngagements, constructor.new(_6167.ClutchEngagementStatus))
        return value

    @property
    def concept_clutch_engagements(self) -> 'List[_6168.ConceptSynchroGearEngagementStatus]':
        '''List[ConceptSynchroGearEngagementStatus]: 'ConceptClutchEngagements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptClutchEngagements, constructor.new(_6168.ConceptSynchroGearEngagementStatus))
        return value
