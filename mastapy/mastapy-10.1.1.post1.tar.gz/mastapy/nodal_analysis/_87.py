'''_87.py

FEMeshingOptions
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _85, _111, _107
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_MESHING_OPTIONS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEMeshingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FEMeshingOptions',)


class FEMeshingOptions(_1.APIBase):
    '''FEMeshingOptions

    This is a mastapy class.
    '''

    TYPE = _FE_MESHING_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEMeshingOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def element_size(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementSize' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementSize) if self.wrapped.ElementSize else None

    @element_size.setter
    def element_size(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementSize = value

    @property
    def element_order(self) -> '_85.ElementOrder':
        '''ElementOrder: 'ElementOrder' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ElementOrder)
        return constructor.new(_85.ElementOrder)(value) if value else None

    @element_order.setter
    def element_order(self, value: '_85.ElementOrder'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ElementOrder = value

    @property
    def element_shape(self) -> '_111.VolumeElementShape':
        '''VolumeElementShape: 'ElementShape' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ElementShape)
        return constructor.new(_111.VolumeElementShape)(value) if value else None

    @element_shape.setter
    def element_shape(self, value: '_111.VolumeElementShape'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ElementShape = value

    @property
    def smooth_corners(self) -> 'bool':
        '''bool: 'SmoothCorners' is the original name of this property.'''

        return self.wrapped.SmoothCorners

    @smooth_corners.setter
    def smooth_corners(self, value: 'bool'):
        self.wrapped.SmoothCorners = bool(value) if value else False

    @property
    def corner_tolerance(self) -> 'float':
        '''float: 'CornerTolerance' is the original name of this property.'''

        return self.wrapped.CornerTolerance

    @corner_tolerance.setter
    def corner_tolerance(self, value: 'float'):
        self.wrapped.CornerTolerance = float(value) if value else 0.0

    @property
    def minimum_fillet_radius_to_include(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumFilletRadiusToInclude' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumFilletRadiusToInclude) if self.wrapped.MinimumFilletRadiusToInclude else None

    @minimum_fillet_radius_to_include.setter
    def minimum_fillet_radius_to_include(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumFilletRadiusToInclude = value

    @property
    def maximum_spanning_angle(self) -> 'float':
        '''float: 'MaximumSpanningAngle' is the original name of this property.'''

        return self.wrapped.MaximumSpanningAngle

    @maximum_spanning_angle.setter
    def maximum_spanning_angle(self, value: 'float'):
        self.wrapped.MaximumSpanningAngle = float(value) if value else 0.0

    @property
    def maximum_chord_height(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumChordHeight' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumChordHeight) if self.wrapped.MaximumChordHeight else None

    @maximum_chord_height.setter
    def maximum_chord_height(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MaximumChordHeight = value

    @property
    def maximum_growth_rate(self) -> 'float':
        '''float: 'MaximumGrowthRate' is the original name of this property.'''

        return self.wrapped.MaximumGrowthRate

    @maximum_growth_rate.setter
    def maximum_growth_rate(self, value: 'float'):
        self.wrapped.MaximumGrowthRate = float(value) if value else 0.0

    @property
    def minimum_triangle_angle(self) -> 'float':
        '''float: 'MinimumTriangleAngle' is the original name of this property.'''

        return self.wrapped.MinimumTriangleAngle

    @minimum_triangle_angle.setter
    def minimum_triangle_angle(self, value: 'float'):
        self.wrapped.MinimumTriangleAngle = float(value) if value else 0.0

    @property
    def maximum_edge_altitude_ratio(self) -> 'float':
        '''float: 'MaximumEdgeAltitudeRatio' is the original name of this property.'''

        return self.wrapped.MaximumEdgeAltitudeRatio

    @maximum_edge_altitude_ratio.setter
    def maximum_edge_altitude_ratio(self, value: 'float'):
        self.wrapped.MaximumEdgeAltitudeRatio = float(value) if value else 0.0

    @property
    def meshing_diameter_for_gear(self) -> '_107.MeshingDiameterForGear':
        '''MeshingDiameterForGear: 'MeshingDiameterForGear' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MeshingDiameterForGear)
        return constructor.new(_107.MeshingDiameterForGear)(value) if value else None

    @meshing_diameter_for_gear.setter
    def meshing_diameter_for_gear(self, value: '_107.MeshingDiameterForGear'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MeshingDiameterForGear = value
