'''_2364.py

StraightBevelPlanetGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2010
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2356
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelPlanetGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearSystemDeflection',)


class StraightBevelPlanetGearSystemDeflection(_2356.StraightBevelDiffGearSystemDeflection):
    '''StraightBevelPlanetGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2010.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2010.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
