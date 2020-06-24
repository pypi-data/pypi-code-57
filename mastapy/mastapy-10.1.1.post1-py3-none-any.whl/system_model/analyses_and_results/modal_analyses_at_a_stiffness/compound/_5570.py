'''_5570.py

CylindricalGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5568, _5569, _5580
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5450
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CylindricalGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundModalAnalysisAtAStiffness',)


class CylindricalGearSetCompoundModalAnalysisAtAStiffness(_5580.GearSetCompoundModalAnalysisAtAStiffness):
    '''CylindricalGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_5568.CylindricalGearCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearCompoundModalAnalysisAtAStiffness]: 'CylindricalGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundModalAnalysisAtAStiffness, constructor.new(_5568.CylindricalGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_5569.CylindricalGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearMeshCompoundModalAnalysisAtAStiffness]: 'CylindricalMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_5569.CylindricalGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5450.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5450.CylindricalGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_5450.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_5450.CylindricalGearSetModalAnalysisAtAStiffness))
        return value
