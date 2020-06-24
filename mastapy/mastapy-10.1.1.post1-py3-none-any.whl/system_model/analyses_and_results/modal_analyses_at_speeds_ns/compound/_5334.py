'''_5334.py

DatumCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1916
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5212
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5312
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'DatumCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundModalAnalysesAtSpeeds',)


class DatumCompoundModalAnalysesAtSpeeds(_5312.ComponentCompoundModalAnalysesAtSpeeds):
    '''DatumCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5212.DatumModalAnalysesAtSpeeds]':
        '''List[DatumModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5212.DatumModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_5212.DatumModalAnalysesAtSpeeds]':
        '''List[DatumModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_5212.DatumModalAnalysesAtSpeeds))
        return value
