'''_3245.py

ConceptGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2061
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6077
from mastapy.gears.rating.concept import _338
from mastapy.system_model.analyses_and_results.power_flows import _3244, _3243, _3270
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetPowerFlow',)


class ConceptGearSetPowerFlow(_3270.GearSetPowerFlow):
    '''ConceptGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetPowerFlow.TYPE'):
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
    def gears_power_flow(self) -> 'List[_3244.ConceptGearPowerFlow]':
        '''List[ConceptGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3244.ConceptGearPowerFlow))
        return value

    @property
    def concept_gears_power_flow(self) -> 'List[_3244.ConceptGearPowerFlow]':
        '''List[ConceptGearPowerFlow]: 'ConceptGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsPowerFlow, constructor.new(_3244.ConceptGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3243.ConceptGearMeshPowerFlow]':
        '''List[ConceptGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3243.ConceptGearMeshPowerFlow))
        return value

    @property
    def concept_meshes_power_flow(self) -> 'List[_3243.ConceptGearMeshPowerFlow]':
        '''List[ConceptGearMeshPowerFlow]: 'ConceptMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesPowerFlow, constructor.new(_3243.ConceptGearMeshPowerFlow))
        return value
