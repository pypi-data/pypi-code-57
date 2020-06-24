'''_3891.py

ExternalCADModelCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3768
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3868
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ExternalCADModelCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundModalAnalysesAtStiffnesses',)


class ExternalCADModelCompoundModalAnalysesAtStiffnesses(_3868.ComponentCompoundModalAnalysesAtStiffnesses):
    '''ExternalCADModelCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3768.ExternalCADModelModalAnalysesAtStiffnesses]':
        '''List[ExternalCADModelModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3768.ExternalCADModelModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3768.ExternalCADModelModalAnalysesAtStiffnesses]':
        '''List[ExternalCADModelModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3768.ExternalCADModelModalAnalysesAtStiffnesses))
        return value
