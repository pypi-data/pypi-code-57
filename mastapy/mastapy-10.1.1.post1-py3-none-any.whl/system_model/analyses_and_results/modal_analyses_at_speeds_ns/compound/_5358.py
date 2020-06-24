'''_5358.py

MassDiscCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1926
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5237
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5400
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'MassDiscCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundModalAnalysesAtSpeeds',)


class MassDiscCompoundModalAnalysesAtSpeeds(_5400.VirtualComponentCompoundModalAnalysesAtSpeeds):
    '''MassDiscCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5237.MassDiscModalAnalysesAtSpeeds]':
        '''List[MassDiscModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5237.MassDiscModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_5237.MassDiscModalAnalysesAtSpeeds]':
        '''List[MassDiscModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_5237.MassDiscModalAnalysesAtSpeeds))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundModalAnalysesAtSpeeds]':
        '''List[MassDiscCompoundModalAnalysesAtSpeeds]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundModalAnalysesAtSpeeds))
        return value
