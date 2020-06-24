'''_6091.py

CylindricalGearLoadCase
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.system_model.part_model.gears import _2064
from mastapy.system_model.analyses_and_results.static_loads import _6092, _6118
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _846
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLoadCase',)


class CylindricalGearLoadCase(_6118.GearLoadCase):
    '''CylindricalGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def override_micro_geometry(self) -> 'bool':
        '''bool: 'OverrideMicroGeometry' is the original name of this property.'''

        return self.wrapped.OverrideMicroGeometry

    @override_micro_geometry.setter
    def override_micro_geometry(self, value: 'bool'):
        self.wrapped.OverrideMicroGeometry = bool(value) if value else False

    @property
    def speed(self) -> 'float':
        '''float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Speed

    @property
    def torque(self) -> 'float':
        '''float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Torque

    @property
    def power(self) -> 'float':
        '''float: 'Power' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Power

    @property
    def reversed_bending_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ReversedBendingFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ReversedBendingFactor) if self.wrapped.ReversedBendingFactor else None

    @reversed_bending_factor.setter
    def reversed_bending_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ReversedBendingFactor = value

    @property
    def lateral_reaction_force(self) -> 'float':
        '''float: 'LateralReactionForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LateralReactionForce

    @property
    def vertical_reaction_force(self) -> 'float':
        '''float: 'VerticalReactionForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VerticalReactionForce

    @property
    def axial_reaction_force(self) -> 'float':
        '''float: 'AxialReactionForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialReactionForce

    @property
    def lateral_reaction_moment(self) -> 'float':
        '''float: 'LateralReactionMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LateralReactionMoment

    @property
    def vertical_reaction_moment(self) -> 'float':
        '''float: 'VerticalReactionMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VerticalReactionMoment

    @property
    def component_design(self) -> '_2064.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def gear_manufacture_errors(self) -> '_6092.CylindricalGearManufactureError':
        '''CylindricalGearManufactureError: 'GearManufactureErrors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6092.CylindricalGearManufactureError)(self.wrapped.GearManufactureErrors) if self.wrapped.GearManufactureErrors else None

    @property
    def overridden_micro_geometry(self) -> '_846.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'OverriddenMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_846.CylindricalGearMicroGeometry)(self.wrapped.OverriddenMicroGeometry) if self.wrapped.OverriddenMicroGeometry else None
