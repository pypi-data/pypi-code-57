'''_1521.py

LoadedBearingDutyCycle
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_designs import _1646, _1647, _1648
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1649, _1650, _1651, _1652,
    _1653, _1654, _1655, _1656,
    _1657, _1658, _1659, _1660,
    _1661, _1662, _1663, _1664
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1665, _1666, _1667, _1668
)
from mastapy.bearings.bearing_designs.concept import _1669, _1670
from mastapy.utility.property import _1448
from mastapy.bearings import _1465
from mastapy.bearings.bearing_results import _1522
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingDutyCycle',)


class LoadedBearingDutyCycle(_1.APIBase):
    '''LoadedBearingDutyCycle

    This is a mastapy class.
    '''

    TYPE = _LOADED_BEARING_DUTY_CYCLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duty_cycle_name(self) -> 'str':
        '''str: 'DutyCycleName' is the original name of this property.'''

        return self.wrapped.DutyCycleName

    @duty_cycle_name.setter
    def duty_cycle_name(self, value: 'str'):
        self.wrapped.DutyCycleName = str(value) if value else None

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Duration

    @property
    def bearing_design(self) -> '_1646.BearingDesign':
        '''BearingDesign: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1646.BearingDesign)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_dummy_rolling_bearing(self) -> '_1647.DummyRollingBearing':
        '''DummyRollingBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'DummyRollingBearing':
            raise CastException('Failed to cast bearing_design to DummyRollingBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1647.DummyRollingBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_linear_bearing(self) -> '_1648.LinearBearing':
        '''LinearBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'LinearBearing':
            raise CastException('Failed to cast bearing_design to LinearBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1648.LinearBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_angular_contact_ball_bearing(self) -> '_1649.AngularContactBallBearing':
        '''AngularContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'AngularContactBallBearing':
            raise CastException('Failed to cast bearing_design to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1649.AngularContactBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_deep_groove_ball_bearing(self) -> '_1650.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'DeepGrooveBallBearing':
            raise CastException('Failed to cast bearing_design to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1650.DeepGrooveBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_self_aligning_ball_bearing(self) -> '_1651.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'SelfAligningBallBearing':
            raise CastException('Failed to cast bearing_design to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1651.SelfAligningBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_thrust_ball_bearing(self) -> '_1652.ThrustBallBearing':
        '''ThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'ThrustBallBearing':
            raise CastException('Failed to cast bearing_design to ThrustBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1652.ThrustBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_angular_contact_thrust_ball_bearing(self) -> '_1653.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'AngularContactThrustBallBearing':
            raise CastException('Failed to cast bearing_design to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1653.AngularContactThrustBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_four_point_contact_ball_bearing(self) -> '_1654.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'FourPointContactBallBearing':
            raise CastException('Failed to cast bearing_design to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1654.FourPointContactBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_three_point_contact_ball_bearing(self) -> '_1655.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'ThreePointContactBallBearing':
            raise CastException('Failed to cast bearing_design to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1655.ThreePointContactBallBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_asymmetric_spherical_roller_bearing(self) -> '_1656.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'AsymmetricSphericalRollerBearing':
            raise CastException('Failed to cast bearing_design to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1656.AsymmetricSphericalRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_spherical_roller_bearing(self) -> '_1657.SphericalRollerBearing':
        '''SphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'SphericalRollerBearing':
            raise CastException('Failed to cast bearing_design to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1657.SphericalRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_spherical_roller_thrust_bearing(self) -> '_1658.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'SphericalRollerThrustBearing':
            raise CastException('Failed to cast bearing_design to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1658.SphericalRollerThrustBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_toroidal_roller_bearing(self) -> '_1659.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'ToroidalRollerBearing':
            raise CastException('Failed to cast bearing_design to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1659.ToroidalRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1660.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'AxialThrustCylindricalRollerBearing':
            raise CastException('Failed to cast bearing_design to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1660.AxialThrustCylindricalRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_cylindrical_roller_bearing(self) -> '_1661.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'CylindricalRollerBearing':
            raise CastException('Failed to cast bearing_design to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1661.CylindricalRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_taper_roller_bearing(self) -> '_1662.TaperRollerBearing':
        '''TaperRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'TaperRollerBearing':
            raise CastException('Failed to cast bearing_design to TaperRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1662.TaperRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_axial_thrust_needle_roller_bearing(self) -> '_1663.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'AxialThrustNeedleRollerBearing':
            raise CastException('Failed to cast bearing_design to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1663.AxialThrustNeedleRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_needle_roller_bearing(self) -> '_1664.NeedleRollerBearing':
        '''NeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'NeedleRollerBearing':
            raise CastException('Failed to cast bearing_design to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1664.NeedleRollerBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_tilting_pad_journal_bearing(self) -> '_1665.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'TiltingPadJournalBearing':
            raise CastException('Failed to cast bearing_design to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1665.TiltingPadJournalBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_tilting_pad_thrust_bearing(self) -> '_1666.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'TiltingPadThrustBearing':
            raise CastException('Failed to cast bearing_design to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1666.TiltingPadThrustBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_plain_grease_filled_journal_bearing(self) -> '_1667.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'PlainGreaseFilledJournalBearing':
            raise CastException('Failed to cast bearing_design to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1667.PlainGreaseFilledJournalBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_plain_oil_fed_journal_bearing(self) -> '_1668.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'PlainOilFedJournalBearing':
            raise CastException('Failed to cast bearing_design to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1668.PlainOilFedJournalBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_concept_axial_clearance_bearing(self) -> '_1669.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'ConceptAxialClearanceBearing':
            raise CastException('Failed to cast bearing_design to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1669.ConceptAxialClearanceBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_concept_radial_clearance_bearing(self) -> '_1670.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.BearingDesign.__class__.__qualname__ != 'ConceptRadialClearanceBearing':
            raise CastException('Failed to cast bearing_design to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new(_1670.ConceptRadialClearanceBearing)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def radial_load_summary(self) -> '_1448.DutyCyclePropertySummaryForce[_1465.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'RadialLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1448.DutyCyclePropertySummaryForce)[_1465.BearingLoadCaseResultsLightweight](self.wrapped.RadialLoadSummary) if self.wrapped.RadialLoadSummary else None

    @property
    def z_thrust_reaction_summary(self) -> '_1448.DutyCyclePropertySummaryForce[_1465.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ZThrustReactionSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1448.DutyCyclePropertySummaryForce)[_1465.BearingLoadCaseResultsLightweight](self.wrapped.ZThrustReactionSummary) if self.wrapped.ZThrustReactionSummary else None

    @property
    def bearing_load_case_results(self) -> 'List[_1522.LoadedBearingResults]':
        '''List[LoadedBearingResults]: 'BearingLoadCaseResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingLoadCaseResults, constructor.new(_1522.LoadedBearingResults))
        return value
