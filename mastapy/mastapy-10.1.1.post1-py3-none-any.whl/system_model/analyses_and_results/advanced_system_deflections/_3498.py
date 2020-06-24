'''_3498.py

StraightBevelSunGearAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3493
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'StraightBevelSunGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearAdvancedSystemDeflection',)


class StraightBevelSunGearAdvancedSystemDeflection(_3493.StraightBevelDiffGearAdvancedSystemDeflection):
    '''StraightBevelSunGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
