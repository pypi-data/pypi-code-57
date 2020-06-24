'''_2725.py

SpiralBevelGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1988
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2723, _2724, _2650
from mastapy.system_model.analyses_and_results.system_deflections import _2354
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SpiralBevelGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundSystemDeflection',)


class SpiralBevelGearSetCompoundSystemDeflection(_2650.BevelGearSetCompoundSystemDeflection):
    '''SpiralBevelGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1988.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1988.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_system_deflection(self) -> 'List[_2723.SpiralBevelGearCompoundSystemDeflection]':
        '''List[SpiralBevelGearCompoundSystemDeflection]: 'SpiralBevelGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundSystemDeflection, constructor.new(_2723.SpiralBevelGearCompoundSystemDeflection))
        return value

    @property
    def spiral_bevel_meshes_compound_system_deflection(self) -> 'List[_2724.SpiralBevelGearMeshCompoundSystemDeflection]':
        '''List[SpiralBevelGearMeshCompoundSystemDeflection]: 'SpiralBevelMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundSystemDeflection, constructor.new(_2724.SpiralBevelGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2354.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2354.SpiralBevelGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2354.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2354.SpiralBevelGearSetSystemDeflection))
        return value
