'''_2236.py

ConceptGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2061
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6077
from mastapy.system_model.analyses_and_results.power_flows import _3245
from mastapy.gears.rating.concept import _338
from mastapy.system_model.analyses_and_results.system_deflections import _2237, _2235, _2268
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSystemDeflection',)


class ConceptGearSetSystemDeflection(_2268.GearSetSystemDeflection):
    '''ConceptGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2061.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2061.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6077.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6077.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3245.ConceptGearSetPowerFlow':
        '''ConceptGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3245.ConceptGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_338.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_338.ConceptGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_338.ConceptGearSetRating':
        '''ConceptGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_338.ConceptGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def concept_gears_system_deflection(self) -> 'List[_2237.ConceptGearSystemDeflection]':
        '''List[ConceptGearSystemDeflection]: 'ConceptGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSystemDeflection, constructor.new(_2237.ConceptGearSystemDeflection))
        return value

    @property
    def concept_meshes_system_deflection(self) -> 'List[_2235.ConceptGearMeshSystemDeflection]':
        '''List[ConceptGearMeshSystemDeflection]: 'ConceptMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSystemDeflection, constructor.new(_2235.ConceptGearMeshSystemDeflection))
        return value
