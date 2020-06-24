'''_3947.py

StraightBevelGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2087
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3945, _3946, _3861
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3826
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'StraightBevelGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundModalAnalysesAtStiffnesses',)


class StraightBevelGearSetCompoundModalAnalysesAtStiffnesses(_3861.BevelGearSetCompoundModalAnalysesAtStiffnesses):
    '''StraightBevelGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2087.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2087.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3945.StraightBevelGearCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearCompoundModalAnalysesAtStiffnesses]: 'StraightBevelGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_3945.StraightBevelGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3946.StraightBevelGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearMeshCompoundModalAnalysesAtStiffnesses]: 'StraightBevelMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_3946.StraightBevelGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3826.StraightBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3826.StraightBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3826.StraightBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3826.StraightBevelGearSetModalAnalysesAtStiffnesses))
        return value
