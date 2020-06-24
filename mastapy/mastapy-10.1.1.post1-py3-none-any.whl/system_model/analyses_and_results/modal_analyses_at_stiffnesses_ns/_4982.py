'''_4982.py

HypoidGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2338
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4981, _4980, _4928
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'HypoidGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetModalAnalysesAtStiffnesses',)


class HypoidGearSetModalAnalysesAtStiffnesses(_4928.AGMAGleasonConicalGearSetModalAnalysesAtStiffnesses):
    '''HypoidGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2338.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2338.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_modal_analyses_at_stiffnesses(self) -> 'List[_4981.HypoidGearModalAnalysesAtStiffnesses]':
        '''List[HypoidGearModalAnalysesAtStiffnesses]: 'HypoidGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsModalAnalysesAtStiffnesses, constructor.new(_4981.HypoidGearModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_4980.HypoidGearMeshModalAnalysesAtStiffnesses]':
        '''List[HypoidGearMeshModalAnalysesAtStiffnesses]: 'HypoidMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesModalAnalysesAtStiffnesses, constructor.new(_4980.HypoidGearMeshModalAnalysesAtStiffnesses))
        return value
