'''_5068.py

ClutchHalfCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2015
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4944
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5084
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ClutchHalfCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundModalAnalysesAtStiffnesses',)


class ClutchHalfCompoundModalAnalysesAtStiffnesses(_5084.CouplingHalfCompoundModalAnalysesAtStiffnesses):
    '''ClutchHalfCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4944.ClutchHalfModalAnalysesAtStiffnesses]':
        '''List[ClutchHalfModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4944.ClutchHalfModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4944.ClutchHalfModalAnalysesAtStiffnesses]':
        '''List[ClutchHalfModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_4944.ClutchHalfModalAnalysesAtStiffnesses))
        return value
