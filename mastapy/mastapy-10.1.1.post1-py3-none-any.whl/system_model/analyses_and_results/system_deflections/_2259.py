'''_2259.py

CylindricalPlanetGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2066
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3261
from mastapy.system_model.analyses_and_results.system_deflections import _2256
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalPlanetGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearSystemDeflection',)


class CylindricalPlanetGearSystemDeflection(_2256.CylindricalGearSystemDeflection):
    '''CylindricalPlanetGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2066.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3261.CylindricalPlanetGearPowerFlow':
        '''CylindricalPlanetGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3261.CylindricalPlanetGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
