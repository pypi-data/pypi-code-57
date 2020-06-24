'''_5361.py

OilSealCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1929
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5242
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5323
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'OilSealCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysesAtSpeeds',)


class OilSealCompoundModalAnalysesAtSpeeds(_5323.ConnectorCompoundModalAnalysesAtSpeeds):
    '''OilSealCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5242.OilSealModalAnalysesAtSpeeds]':
        '''List[OilSealModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5242.OilSealModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_5242.OilSealModalAnalysesAtSpeeds]':
        '''List[OilSealModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_5242.OilSealModalAnalysesAtSpeeds))
        return value
