'''_5105.py

ImportedFEComponentCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1924
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4983
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5048
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ImportedFEComponentCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundModalAnalysesAtStiffnesses',)


class ImportedFEComponentCompoundModalAnalysesAtStiffnesses(_5048.AbstractShaftOrHousingCompoundModalAnalysesAtStiffnesses):
    '''ImportedFEComponentCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4983.ImportedFEComponentModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4983.ImportedFEComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4983.ImportedFEComponentModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_4983.ImportedFEComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentCompoundModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundModalAnalysesAtStiffnesses))
        return value
