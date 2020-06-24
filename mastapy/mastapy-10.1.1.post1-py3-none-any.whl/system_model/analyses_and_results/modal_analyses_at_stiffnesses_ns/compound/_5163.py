'''_5163.py

WormGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1970
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5161, _5162, _5100
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5043
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'WormGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundModalAnalysesAtStiffnesses',)


class WormGearSetCompoundModalAnalysesAtStiffnesses(_5100.GearSetCompoundModalAnalysesAtStiffnesses):
    '''WormGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1970.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1970.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1970.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1970.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5161.WormGearCompoundModalAnalysesAtStiffnesses]':
        '''List[WormGearCompoundModalAnalysesAtStiffnesses]: 'WormGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_5161.WormGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5162.WormGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[WormGearMeshCompoundModalAnalysesAtStiffnesses]: 'WormMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_5162.WormGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5043.WormGearSetModalAnalysesAtStiffnesses]':
        '''List[WormGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5043.WormGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5043.WormGearSetModalAnalysesAtStiffnesses]':
        '''List[WormGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_5043.WormGearSetModalAnalysesAtStiffnesses))
        return value
