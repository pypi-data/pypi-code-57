'''_5054.py

BeltConnectionCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1760
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4931
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5106
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'BeltConnectionCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundModalAnalysesAtStiffnesses',)


class BeltConnectionCompoundModalAnalysesAtStiffnesses(_5106.InterMountableComponentConnectionCompoundModalAnalysesAtStiffnesses):
    '''BeltConnectionCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1760.BeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1760.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4931.BeltConnectionModalAnalysesAtStiffnesses]':
        '''List[BeltConnectionModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4931.BeltConnectionModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4931.BeltConnectionModalAnalysesAtStiffnesses]':
        '''List[BeltConnectionModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_4931.BeltConnectionModalAnalysesAtStiffnesses))
        return value
