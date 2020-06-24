'''_5058.py

BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5056, _5057, _5063
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4935
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses',)


class BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses(_5063.BevelGearSetCompoundModalAnalysesAtStiffnesses):
    '''BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5056.BevelDifferentialGearCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_5056.BevelDifferentialGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5057.BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_5057.BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4935.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4935.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4935.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_4935.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value
