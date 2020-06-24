'''_3995.py

ConceptGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2061
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6077
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3994, _3993, _4020
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ConceptGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetModalAnalysesAtSpeeds',)


class ConceptGearSetModalAnalysesAtSpeeds(_4020.GearSetModalAnalysesAtSpeeds):
    '''ConceptGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetModalAnalysesAtSpeeds.TYPE'):
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
    def concept_gears_modal_analyses_at_speeds(self) -> 'List[_3994.ConceptGearModalAnalysesAtSpeeds]':
        '''List[ConceptGearModalAnalysesAtSpeeds]: 'ConceptGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsModalAnalysesAtSpeeds, constructor.new(_3994.ConceptGearModalAnalysesAtSpeeds))
        return value

    @property
    def concept_meshes_modal_analyses_at_speeds(self) -> 'List[_3993.ConceptGearMeshModalAnalysesAtSpeeds]':
        '''List[ConceptGearMeshModalAnalysesAtSpeeds]: 'ConceptMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesModalAnalysesAtSpeeds, constructor.new(_3993.ConceptGearMeshModalAnalysesAtSpeeds))
        return value
