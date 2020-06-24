'''_766.py

CaseHardeningPropertiesForFEAnalysis
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _806
from mastapy.utility import _1126
from mastapy._internal.python_net import python_net_import

_CASE_HARDENING_PROPERTIES_FOR_FE_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CaseHardeningPropertiesForFEAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CaseHardeningPropertiesForFEAnalysis',)


class CaseHardeningPropertiesForFEAnalysis(_1126.CachedIndependentReportablePropertiesBase['CaseHardeningPropertiesForFEAnalysis']):
    '''CaseHardeningPropertiesForFEAnalysis

    This is a mastapy class.
    '''

    TYPE = _CASE_HARDENING_PROPERTIES_FOR_FE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CaseHardeningPropertiesForFEAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def total_case_depth(self) -> 'float':
        '''float: 'TotalCaseDepth' is the original name of this property.'''

        return self.wrapped.TotalCaseDepth

    @total_case_depth.setter
    def total_case_depth(self, value: 'float'):
        self.wrapped.TotalCaseDepth = float(value) if value else 0.0

    @property
    def include_shot_peening(self) -> 'bool':
        '''bool: 'IncludeShotPeening' is the original name of this property.'''

        return self.wrapped.IncludeShotPeening

    @include_shot_peening.setter
    def include_shot_peening(self, value: 'bool'):
        self.wrapped.IncludeShotPeening = bool(value) if value else False

    @property
    def shot_peening_depth(self) -> 'float':
        '''float: 'ShotPeeningDepth' is the original name of this property.'''

        return self.wrapped.ShotPeeningDepth

    @shot_peening_depth.setter
    def shot_peening_depth(self, value: 'float'):
        self.wrapped.ShotPeeningDepth = float(value) if value else 0.0

    @property
    def shot_peening_factor(self) -> 'float':
        '''float: 'ShotPeeningFactor' is the original name of this property.'''

        return self.wrapped.ShotPeeningFactor

    @shot_peening_factor.setter
    def shot_peening_factor(self, value: 'float'):
        self.wrapped.ShotPeeningFactor = float(value) if value else 0.0

    @property
    def include_residual_stresses(self) -> 'bool':
        '''bool: 'IncludeResidualStresses' is the original name of this property.'''

        return self.wrapped.IncludeResidualStresses

    @include_residual_stresses.setter
    def include_residual_stresses(self, value: 'bool'):
        self.wrapped.IncludeResidualStresses = bool(value) if value else False

    @property
    def strain_at_surface(self) -> 'float':
        '''float: 'StrainAtSurface' is the original name of this property.'''

        return self.wrapped.StrainAtSurface

    @strain_at_surface.setter
    def strain_at_surface(self, value: 'float'):
        self.wrapped.StrainAtSurface = float(value) if value else 0.0

    @property
    def strain_at_mid_case_depth(self) -> 'float':
        '''float: 'StrainAtMidCaseDepth' is the original name of this property.'''

        return self.wrapped.StrainAtMidCaseDepth

    @strain_at_mid_case_depth.setter
    def strain_at_mid_case_depth(self, value: 'float'):
        self.wrapped.StrainAtMidCaseDepth = float(value) if value else 0.0

    @property
    def surface_material_properties(self) -> '_806.HardenedMaterialProperties':
        '''HardenedMaterialProperties: 'SurfaceMaterialProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_806.HardenedMaterialProperties)(self.wrapped.SurfaceMaterialProperties) if self.wrapped.SurfaceMaterialProperties else None

    @property
    def core_material_properties(self) -> '_806.HardenedMaterialProperties':
        '''HardenedMaterialProperties: 'CoreMaterialProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_806.HardenedMaterialProperties)(self.wrapped.CoreMaterialProperties) if self.wrapped.CoreMaterialProperties else None
