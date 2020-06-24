'''_3872.py

ConceptGearCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2060
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3749
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3896
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ConceptGearCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundModalAnalysesAtStiffnesses',)


class ConceptGearCompoundModalAnalysesAtStiffnesses(_3896.GearCompoundModalAnalysesAtStiffnesses):
    '''ConceptGearCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2060.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2060.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3749.ConceptGearModalAnalysesAtStiffnesses]':
        '''List[ConceptGearModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3749.ConceptGearModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3749.ConceptGearModalAnalysesAtStiffnesses]':
        '''List[ConceptGearModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3749.ConceptGearModalAnalysesAtStiffnesses))
        return value
