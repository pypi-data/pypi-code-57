'''_4118.py

ConceptGearCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2060
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3994
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4142
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ConceptGearCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundModalAnalysesAtSpeeds',)


class ConceptGearCompoundModalAnalysesAtSpeeds(_4142.GearCompoundModalAnalysesAtSpeeds):
    '''ConceptGearCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2060.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2060.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3994.ConceptGearModalAnalysesAtSpeeds]':
        '''List[ConceptGearModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3994.ConceptGearModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_3994.ConceptGearModalAnalysesAtSpeeds]':
        '''List[ConceptGearModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_3994.ConceptGearModalAnalysesAtSpeeds))
        return value
