'''_3833.py

CylindricalPlanetGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2014
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2329
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3831
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CylindricalPlanetGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearGearWhineAnalysis',)


class CylindricalPlanetGearGearWhineAnalysis(_3831.CylindricalGearGearWhineAnalysis):
    '''CylindricalPlanetGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2329.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2329.CylindricalPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
