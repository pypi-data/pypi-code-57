'''_3474.py

CylindricalPlanetGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3472
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CylindricalPlanetGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearDynamicAnalysis',)


class CylindricalPlanetGearDynamicAnalysis(_3472.CylindricalGearDynamicAnalysis):
    '''CylindricalPlanetGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1986.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
