'''_2148.py

BevelDifferentialSunGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2146
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BevelDifferentialSunGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearSystemDeflection',)


class BevelDifferentialSunGearSystemDeflection(_2146.BevelDifferentialGearSystemDeflection):
    '''BevelDifferentialSunGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
