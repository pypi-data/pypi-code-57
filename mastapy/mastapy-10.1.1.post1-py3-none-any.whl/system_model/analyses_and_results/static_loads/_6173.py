'''_6173.py

ShaftHubConnectionLoadCase
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2132
from mastapy.system_model.analyses_and_results.static_loads import _6084
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftHubConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionLoadCase',)


class ShaftHubConnectionLoadCase(_6084.ConnectorLoadCase):
    '''ShaftHubConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def torsional_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TorsionalStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TorsionalStiffness) if self.wrapped.TorsionalStiffness else None

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TorsionalStiffness = value

    @property
    def additional_tilt_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AdditionalTiltStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AdditionalTiltStiffness) if self.wrapped.AdditionalTiltStiffness else None

    @additional_tilt_stiffness.setter
    def additional_tilt_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AdditionalTiltStiffness = value

    @property
    def tilt_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TiltStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TiltStiffness) if self.wrapped.TiltStiffness else None

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TiltStiffness = value

    @property
    def radial_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialStiffness) if self.wrapped.RadialStiffness else None

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RadialStiffness = value

    @property
    def axial_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialStiffness) if self.wrapped.AxialStiffness else None

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AxialStiffness = value

    @property
    def radial_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialClearance) if self.wrapped.RadialClearance else None

    @radial_clearance.setter
    def radial_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RadialClearance = value

    @property
    def tilt_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TiltClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TiltClearance) if self.wrapped.TiltClearance else None

    @tilt_clearance.setter
    def tilt_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TiltClearance = value

    @property
    def specified_application_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedApplicationFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedApplicationFactor) if self.wrapped.SpecifiedApplicationFactor else None

    @specified_application_factor.setter
    def specified_application_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpecifiedApplicationFactor = value

    @property
    def specified_backlash_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedBacklashFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedBacklashFactor) if self.wrapped.SpecifiedBacklashFactor else None

    @specified_backlash_factor.setter
    def specified_backlash_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpecifiedBacklashFactor = value

    @property
    def specified_load_distribution_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedLoadDistributionFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedLoadDistributionFactor) if self.wrapped.SpecifiedLoadDistributionFactor else None

    @specified_load_distribution_factor.setter
    def specified_load_distribution_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpecifiedLoadDistributionFactor = value

    @property
    def specified_load_sharing_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedLoadSharingFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedLoadSharingFactor) if self.wrapped.SpecifiedLoadSharingFactor else None

    @specified_load_sharing_factor.setter
    def specified_load_sharing_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpecifiedLoadSharingFactor = value

    @property
    def load_distribution_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LoadDistributionFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LoadDistributionFactor) if self.wrapped.LoadDistributionFactor else None

    @load_distribution_factor.setter
    def load_distribution_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LoadDistributionFactor = value

    @property
    def torsional_twist_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TorsionalTwistPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TorsionalTwistPreload) if self.wrapped.TorsionalTwistPreload else None

    @torsional_twist_preload.setter
    def torsional_twist_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TorsionalTwistPreload = value

    @property
    def axial_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialPreload) if self.wrapped.AxialPreload else None

    @axial_preload.setter
    def axial_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AxialPreload = value

    @property
    def application_factor(self) -> 'float':
        '''float: 'ApplicationFactor' is the original name of this property.'''

        return self.wrapped.ApplicationFactor

    @application_factor.setter
    def application_factor(self, value: 'float'):
        self.wrapped.ApplicationFactor = float(value) if value else 0.0

    @property
    def load_distribution_factor_single_key(self) -> 'float':
        '''float: 'LoadDistributionFactorSingleKey' is the original name of this property.'''

        return self.wrapped.LoadDistributionFactorSingleKey

    @load_distribution_factor_single_key.setter
    def load_distribution_factor_single_key(self, value: 'float'):
        self.wrapped.LoadDistributionFactorSingleKey = float(value) if value else 0.0

    @property
    def number_of_torque_reversals(self) -> 'float':
        '''float: 'NumberOfTorqueReversals' is the original name of this property.'''

        return self.wrapped.NumberOfTorqueReversals

    @number_of_torque_reversals.setter
    def number_of_torque_reversals(self, value: 'float'):
        self.wrapped.NumberOfTorqueReversals = float(value) if value else 0.0

    @property
    def number_of_torque_peaks(self) -> 'float':
        '''float: 'NumberOfTorquePeaks' is the original name of this property.'''

        return self.wrapped.NumberOfTorquePeaks

    @number_of_torque_peaks.setter
    def number_of_torque_peaks(self, value: 'float'):
        self.wrapped.NumberOfTorquePeaks = float(value) if value else 0.0

    @property
    def component_design(self) -> '_2132.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
