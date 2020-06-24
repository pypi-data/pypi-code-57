'''_5124.py

PointLoadCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5004
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5160
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PointLoadCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundModalAnalysesAtStiffnesses',)


class PointLoadCompoundModalAnalysesAtStiffnesses(_5160.VirtualComponentCompoundModalAnalysesAtStiffnesses):
    '''PointLoadCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5004.PointLoadModalAnalysesAtStiffnesses]':
        '''List[PointLoadModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5004.PointLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5004.PointLoadModalAnalysesAtStiffnesses]':
        '''List[PointLoadModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_5004.PointLoadModalAnalysesAtStiffnesses))
        return value
