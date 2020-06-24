'''_2471.py

WormGearCompoundSystemDeflection
'''


from typing import List

from mastapy.gears.rating.worm import _174
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2090
from mastapy.system_model.analyses_and_results.system_deflections import _2342
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2406
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'WormGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundSystemDeflection',)


class WormGearCompoundSystemDeflection(_2406.GearCompoundSystemDeflection):
    '''WormGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duty_cycle_rating(self) -> '_174.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.WormGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def worm_duty_cycle_rating(self) -> '_174.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'WormDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.WormGearDutyCycleRating)(self.wrapped.WormDutyCycleRating) if self.wrapped.WormDutyCycleRating else None

    @property
    def component_design(self) -> '_2090.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2342.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2342.WormGearSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2342.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2342.WormGearSystemDeflection))
        return value
