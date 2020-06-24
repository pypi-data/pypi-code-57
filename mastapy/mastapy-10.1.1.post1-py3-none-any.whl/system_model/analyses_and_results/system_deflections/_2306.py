'''_2306.py

ShaftSectionEndResultsSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1118
from mastapy.shafts import _16
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_SECTION_END_RESULTS_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ShaftSectionEndResultsSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSectionEndResultsSystemDeflection',)


class ShaftSectionEndResultsSystemDeflection(_0.APIBase):
    '''ShaftSectionEndResultsSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SECTION_END_RESULTS_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSectionEndResultsSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Offset

    @property
    def inner_diameter(self) -> 'float':
        '''float: 'InnerDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerDiameter

    @property
    def outer_diameter(self) -> 'float':
        '''float: 'OuterDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterDiameter

    @property
    def cross_sectional_area(self) -> 'float':
        '''float: 'CrossSectionalArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CrossSectionalArea

    @property
    def polar_area_moment_of_inertia(self) -> 'float':
        '''float: 'PolarAreaMomentOfInertia' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PolarAreaMomentOfInertia

    @property
    def surface_roughness(self) -> 'float':
        '''float: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SurfaceRoughness

    @property
    def displacements(self) -> '_1118.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'Displacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1118.VectorWithLinearAndAngularComponents)(self.wrapped.Displacements) if self.wrapped.Displacements else None

    @property
    def forces(self) -> '_1118.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'Forces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1118.VectorWithLinearAndAngularComponents)(self.wrapped.Forces) if self.wrapped.Forces else None

    @property
    def din743201212_total_influence_factor(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212TotalInfluenceFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212TotalInfluenceFactor) if self.wrapped.DIN743201212TotalInfluenceFactor else None

    @property
    def din743201212_increase_factor_for_yield_strength(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212IncreaseFactorForYieldStrength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212IncreaseFactorForYieldStrength) if self.wrapped.DIN743201212IncreaseFactorForYieldStrength else None

    @property
    def din743201212_static_support_effect_factor(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212StaticSupportEffectFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212StaticSupportEffectFactor) if self.wrapped.DIN743201212StaticSupportEffectFactor else None

    @property
    def din743201212_geometrical_influence_factor_for_size_k_2d(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212GeometricalInfluenceFactorForSizeK2d' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212GeometricalInfluenceFactorForSizeK2d) if self.wrapped.DIN743201212GeometricalInfluenceFactorForSizeK2d else None

    @property
    def din743201212_surface_roughness_influence_factor(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212SurfaceRoughnessInfluenceFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212SurfaceRoughnessInfluenceFactor) if self.wrapped.DIN743201212SurfaceRoughnessInfluenceFactor else None

    @property
    def din743201212_notch_factor(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212NotchFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_16.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212NotchFactor) if self.wrapped.DIN743201212NotchFactor else None
