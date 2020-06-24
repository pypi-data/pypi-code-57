'''_3295.py

PlanetaryGearSetPowerFlow
'''


from mastapy.system_model.part_model.gears import _2081
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3260
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetaryGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetPowerFlow',)


class PlanetaryGearSetPowerFlow(_3260.CylindricalGearSetPowerFlow):
    '''PlanetaryGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2081.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
