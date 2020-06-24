'''_6248.py

BevelDifferentialSunGearAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2057
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6244
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BevelDifferentialSunGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearAdvancedSystemDeflection',)


class BevelDifferentialSunGearAdvancedSystemDeflection(_6244.BevelDifferentialGearAdvancedSystemDeflection):
    '''BevelDifferentialSunGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2057.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2057.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
