'''_2330.py

CylindricalPlanetGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2014
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2326
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalPlanetGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearLoadCase',)


class CylindricalPlanetGearLoadCase(_2326.CylindricalGearLoadCase):
    '''CylindricalPlanetGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
