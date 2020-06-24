'''_2295.py

PointLoadLoadCase
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy.system_model.part_model import _1933
from mastapy.nodal_analysis.varying_input_components import _121, _122
from mastapy.system_model.analyses_and_results.static_loads import _6240, _2305
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PointLoadLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadLoadCase',)


class PointLoadLoadCase(_2305.VirtualComponentLoadCase):
    '''PointLoadLoadCase

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def tangential_load(self) -> 'float':
        '''float: 'TangentialLoad' is the original name of this property.'''

        return self.wrapped.TangentialLoad

    @tangential_load.setter
    def tangential_load(self, value: 'float'):
        self.wrapped.TangentialLoad = float(value) if value else 0.0

    @property
    def radial_load(self) -> 'float':
        '''float: 'RadialLoad' is the original name of this property.'''

        return self.wrapped.RadialLoad

    @radial_load.setter
    def radial_load(self, value: 'float'):
        self.wrapped.RadialLoad = float(value) if value else 0.0

    @property
    def magnitude_radial_force(self) -> 'float':
        '''float: 'MagnitudeRadialForce' is the original name of this property.'''

        return self.wrapped.MagnitudeRadialForce

    @magnitude_radial_force.setter
    def magnitude_radial_force(self, value: 'float'):
        self.wrapped.MagnitudeRadialForce = float(value) if value else 0.0

    @property
    def angle_of_radial_force(self) -> 'float':
        '''float: 'AngleOfRadialForce' is the original name of this property.'''

        return self.wrapped.AngleOfRadialForce

    @angle_of_radial_force.setter
    def angle_of_radial_force(self, value: 'float'):
        self.wrapped.AngleOfRadialForce = float(value) if value else 0.0

    @property
    def twist_theta_z(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TwistThetaZ' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TwistThetaZ) if self.wrapped.TwistThetaZ else None

    @twist_theta_z.setter
    def twist_theta_z(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TwistThetaZ = value

    @property
    def twist_theta_x(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TwistThetaX' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TwistThetaX) if self.wrapped.TwistThetaX else None

    @twist_theta_x.setter
    def twist_theta_x(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TwistThetaX = value

    @property
    def twist_theta_y(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TwistThetaY' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TwistThetaY) if self.wrapped.TwistThetaY else None

    @twist_theta_y.setter
    def twist_theta_y(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TwistThetaY = value

    @property
    def displacement_x(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DisplacementX' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DisplacementX) if self.wrapped.DisplacementX else None

    @displacement_x.setter
    def displacement_x(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DisplacementX = value

    @property
    def displacement_y(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DisplacementY' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DisplacementY) if self.wrapped.DisplacementY else None

    @displacement_y.setter
    def displacement_y(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DisplacementY = value

    @property
    def displacement_z(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DisplacementZ' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DisplacementZ) if self.wrapped.DisplacementZ else None

    @displacement_z.setter
    def displacement_z(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DisplacementZ = value

    @property
    def force_specification_options(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification':
        '''enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification: 'ForceSpecificationOptions' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification)(self.wrapped.ForceSpecificationOptions) if self.wrapped.ForceSpecificationOptions else None

    @force_specification_options.setter
    def force_specification_options(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ForceSpecificationOptions = value

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def force_x(self) -> '_121.ForceInputComponent':
        '''ForceInputComponent: 'ForceX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_121.ForceInputComponent)(self.wrapped.ForceX) if self.wrapped.ForceX else None

    @property
    def force_y(self) -> '_121.ForceInputComponent':
        '''ForceInputComponent: 'ForceY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_121.ForceInputComponent)(self.wrapped.ForceY) if self.wrapped.ForceY else None

    @property
    def axial_load(self) -> '_121.ForceInputComponent':
        '''ForceInputComponent: 'AxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_121.ForceInputComponent)(self.wrapped.AxialLoad) if self.wrapped.AxialLoad else None

    @property
    def moment_x(self) -> '_122.MomentInputComponent':
        '''MomentInputComponent: 'MomentX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_122.MomentInputComponent)(self.wrapped.MomentX) if self.wrapped.MomentX else None

    @property
    def moment_y(self) -> '_122.MomentInputComponent':
        '''MomentInputComponent: 'MomentY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_122.MomentInputComponent)(self.wrapped.MomentY) if self.wrapped.MomentY else None

    @property
    def moment_z(self) -> '_122.MomentInputComponent':
        '''MomentInputComponent: 'MomentZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_122.MomentInputComponent)(self.wrapped.MomentZ) if self.wrapped.MomentZ else None

    def get_harmonic_load_data_for_import(self) -> '_6240.PointLoadHarmonicLoadData':
        ''' 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadHarmonicLoadData
        '''

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        return constructor.new(_6240.PointLoadHarmonicLoadData)(method_result) if method_result else None
