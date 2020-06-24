'''_5123.py

PlanetCarrierCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5003
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5118
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PlanetCarrierCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundModalAnalysesAtStiffnesses',)


class PlanetCarrierCompoundModalAnalysesAtStiffnesses(_5118.MountableComponentCompoundModalAnalysesAtStiffnesses):
    '''PlanetCarrierCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5003.PlanetCarrierModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5003.PlanetCarrierModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5003.PlanetCarrierModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_5003.PlanetCarrierModalAnalysesAtStiffnesses))
        return value
