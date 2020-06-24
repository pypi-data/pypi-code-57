'''_3228.py

BevelDifferentialPlanetGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2056
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3226
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BevelDifferentialPlanetGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearPowerFlow',)


class BevelDifferentialPlanetGearPowerFlow(_3226.BevelDifferentialGearPowerFlow):
    '''BevelDifferentialPlanetGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2056.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
