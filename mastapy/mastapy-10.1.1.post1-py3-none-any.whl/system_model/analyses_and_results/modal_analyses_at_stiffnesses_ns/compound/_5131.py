'''_5131.py

ShaftCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5012
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5048
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ShaftCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundModalAnalysesAtStiffnesses',)


class ShaftCompoundModalAnalysesAtStiffnesses(_5048.AbstractShaftOrHousingCompoundModalAnalysesAtStiffnesses):
    '''ShaftCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5012.ShaftModalAnalysesAtStiffnesses]':
        '''List[ShaftModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5012.ShaftModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5012.ShaftModalAnalysesAtStiffnesses]':
        '''List[ShaftModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_5012.ShaftModalAnalysesAtStiffnesses))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundModalAnalysesAtStiffnesses]':
        '''List[ShaftCompoundModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundModalAnalysesAtStiffnesses))
        return value
