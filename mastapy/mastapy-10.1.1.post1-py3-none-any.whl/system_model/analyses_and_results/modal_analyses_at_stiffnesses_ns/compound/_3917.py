'''_3917.py

OilSealCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _2008
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3796
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3879
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'OilSealCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysesAtStiffnesses',)


class OilSealCompoundModalAnalysesAtStiffnesses(_3879.ConnectorCompoundModalAnalysesAtStiffnesses):
    '''OilSealCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2008.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2008.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3796.OilSealModalAnalysesAtStiffnesses]':
        '''List[OilSealModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3796.OilSealModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3796.OilSealModalAnalysesAtStiffnesses]':
        '''List[OilSealModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3796.OilSealModalAnalysesAtStiffnesses))
        return value
