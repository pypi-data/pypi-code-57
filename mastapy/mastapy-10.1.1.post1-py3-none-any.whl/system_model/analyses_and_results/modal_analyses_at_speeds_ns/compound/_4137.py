'''_4137.py

ExternalCADModelCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4013
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4114
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ExternalCADModelCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundModalAnalysesAtSpeeds',)


class ExternalCADModelCompoundModalAnalysesAtSpeeds(_4114.ComponentCompoundModalAnalysesAtSpeeds):
    '''ExternalCADModelCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4013.ExternalCADModelModalAnalysesAtSpeeds]':
        '''List[ExternalCADModelModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4013.ExternalCADModelModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_4013.ExternalCADModelModalAnalysesAtSpeeds]':
        '''List[ExternalCADModelModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_4013.ExternalCADModelModalAnalysesAtSpeeds))
        return value
