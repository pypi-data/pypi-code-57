'''_5092.py

DatumCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1916
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4970
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5070
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'DatumCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundModalAnalysesAtStiffnesses',)


class DatumCompoundModalAnalysesAtStiffnesses(_5070.ComponentCompoundModalAnalysesAtStiffnesses):
    '''DatumCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4970.DatumModalAnalysesAtStiffnesses]':
        '''List[DatumModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4970.DatumModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4970.DatumModalAnalysesAtStiffnesses]':
        '''List[DatumModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_4970.DatumModalAnalysesAtStiffnesses))
        return value
