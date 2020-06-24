'''_969.py

CrossedAxisCylindricalGearPair
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _681
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CrossedAxisCylindricalGearPair')


__docformat__ = 'restructuredtext en'
__all__ = ('CrossedAxisCylindricalGearPair',)


class CrossedAxisCylindricalGearPair(_1.APIBase):
    '''CrossedAxisCylindricalGearPair

    This is a mastapy class.
    '''

    TYPE = _CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CrossedAxisCylindricalGearPair.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def centre_distance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CentreDistance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CentreDistance) if self.wrapped.CentreDistance else None

    @centre_distance.setter
    def centre_distance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CentreDistance = value

    @property
    def gear_operating_radius(self) -> 'float':
        '''float: 'GearOperatingRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearOperatingRadius

    @property
    def shaver_operating_radius(self) -> 'float':
        '''float: 'ShaverOperatingRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverOperatingRadius

    @property
    def shaft_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaftAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaftAngle) if self.wrapped.ShaftAngle else None

    @shaft_angle.setter
    def shaft_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ShaftAngle = value

    @property
    def effective_gear_start_of_active_profile_diameter(self) -> 'float':
        '''float: 'EffectiveGearStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EffectiveGearStartOfActiveProfileDiameter

    @property
    def gear_end_of_active_profile_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'GearEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.GearEndOfActiveProfileDiameter) if self.wrapped.GearEndOfActiveProfileDiameter else None

    @property
    def shaver_end_of_active_profile_diameter(self) -> 'float':
        '''float: 'ShaverEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverEndOfActiveProfileDiameter

    @property
    def shaver_required_end_of_active_profile_diameter(self) -> 'float':
        '''float: 'ShaverRequiredEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverRequiredEndOfActiveProfileDiameter

    @property
    def shaver_start_of_active_profile_diameter(self) -> 'float':
        '''float: 'ShaverStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverStartOfActiveProfileDiameter

    @property
    def shaver_tip_radius_calculated_by_gear_sap(self) -> 'float':
        '''float: 'ShaverTipRadiusCalculatedByGearSAP' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverTipRadiusCalculatedByGearSAP

    @property
    def gear_start_of_active_profile_diameter(self) -> 'float':
        '''float: 'GearStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearStartOfActiveProfileDiameter

    @property
    def shaver_tip_radius(self) -> 'float':
        '''float: 'ShaverTipRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverTipRadius

    @property
    def shaver_tip_diameter(self) -> 'float':
        '''float: 'ShaverTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverTipDiameter

    @property
    def contact_ratio(self) -> 'float':
        '''float: 'ContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactRatio

    @property
    def operating_normal_pressure_angle(self) -> 'float':
        '''float: 'OperatingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OperatingNormalPressureAngle

    @property
    def gear_normal_pressure_angle(self) -> 'float':
        '''float: 'GearNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearNormalPressureAngle

    @property
    def cutter_normal_pressure_angle(self) -> 'float':
        '''float: 'CutterNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterNormalPressureAngle

    @property
    def shaver(self) -> '_681.CylindricalCutterSimulatableGear':
        '''CylindricalCutterSimulatableGear: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_681.CylindricalCutterSimulatableGear)(self.wrapped.Shaver) if self.wrapped.Shaver else None
