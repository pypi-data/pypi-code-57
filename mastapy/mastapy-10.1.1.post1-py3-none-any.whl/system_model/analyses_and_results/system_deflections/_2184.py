'''_2184.py

CylindricalGearSetSystemDeflectionWithLTCAResults
'''


from mastapy.gears.ltca.cylindrical import _876
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2182
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearSetSystemDeflectionWithLTCAResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetSystemDeflectionWithLTCAResults',)


class CylindricalGearSetSystemDeflectionWithLTCAResults(_2182.CylindricalGearSetSystemDeflection):
    '''CylindricalGearSetSystemDeflectionWithLTCAResults

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetSystemDeflectionWithLTCAResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def basic_ltca_results(self) -> '_876.CylindricalGearSetLoadDistributionAnalysis':
        '''CylindricalGearSetLoadDistributionAnalysis: 'BasicLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.CylindricalGearSetLoadDistributionAnalysis)(self.wrapped.BasicLTCAResults) if self.wrapped.BasicLTCAResults else None

    @property
    def basic_ltca_results_only_first_planetary_mesh(self) -> '_876.CylindricalGearSetLoadDistributionAnalysis':
        '''CylindricalGearSetLoadDistributionAnalysis: 'BasicLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.CylindricalGearSetLoadDistributionAnalysis)(self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh else None

    @property
    def advanced_ltca_results(self) -> '_876.CylindricalGearSetLoadDistributionAnalysis':
        '''CylindricalGearSetLoadDistributionAnalysis: 'AdvancedLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.CylindricalGearSetLoadDistributionAnalysis)(self.wrapped.AdvancedLTCAResults) if self.wrapped.AdvancedLTCAResults else None

    @property
    def advanced_ltca_results_only_first_planetary_mesh(self) -> '_876.CylindricalGearSetLoadDistributionAnalysis':
        '''CylindricalGearSetLoadDistributionAnalysis: 'AdvancedLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.CylindricalGearSetLoadDistributionAnalysis)(self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh else None
