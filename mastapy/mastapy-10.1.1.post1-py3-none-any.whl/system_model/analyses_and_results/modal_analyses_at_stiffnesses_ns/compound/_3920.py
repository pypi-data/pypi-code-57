'''_3920.py

PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1900
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3798
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3881
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses',)


class PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses(_3881.CouplingConnectionCompoundModalAnalysesAtStiffnesses):
    '''PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3798.PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3798.PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3798.PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_3798.PartToPartShearCouplingConnectionModalAnalysesAtStiffnesses))
        return value
