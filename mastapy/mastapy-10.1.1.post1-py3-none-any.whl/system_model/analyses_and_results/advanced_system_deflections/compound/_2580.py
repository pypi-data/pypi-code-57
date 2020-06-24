'''_2580.py

CylindricalGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.rating.cylindrical import _368
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _1985
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2579, _2647, _2583
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3119
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'CylindricalGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundAdvancedSystemDeflection',)


class CylindricalGearSetCompoundAdvancedSystemDeflection(_2583.GearSetCompoundAdvancedSystemDeflection):
    '''CylindricalGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_duty_cycle_rating(self) -> '_368.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.CylindricalGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def cylindrical_gear_duty_cycle_rating(self) -> '_368.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearDutyCycleRating) if self.wrapped.CylindricalGearDutyCycleRating else None

    @property
    def component_design(self) -> '_1985.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1985.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_advanced_system_deflection(self) -> 'List[_2579.CylindricalGearCompoundAdvancedSystemDeflection]':
        '''List[CylindricalGearCompoundAdvancedSystemDeflection]: 'CylindricalGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundAdvancedSystemDeflection, constructor.new(_2579.CylindricalGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_meshes_compound_advanced_system_deflection(self) -> 'List[_2647.CylindricalGearMeshCompoundAdvancedSystemDeflection]':
        '''List[CylindricalGearMeshCompoundAdvancedSystemDeflection]: 'CylindricalMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundAdvancedSystemDeflection, constructor.new(_2647.CylindricalGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3119.CylindricalGearSetAdvancedSystemDeflection]':
        '''List[CylindricalGearSetAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3119.CylindricalGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_3119.CylindricalGearSetAdvancedSystemDeflection]':
        '''List[CylindricalGearSetAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_3119.CylindricalGearSetAdvancedSystemDeflection))
        return value
