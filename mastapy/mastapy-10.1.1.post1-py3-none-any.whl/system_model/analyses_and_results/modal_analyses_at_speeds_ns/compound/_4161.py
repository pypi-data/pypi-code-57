'''_4161.py

MeasurementComponentCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _2005
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4037
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4205
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'MeasurementComponentCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundModalAnalysesAtSpeeds',)


class MeasurementComponentCompoundModalAnalysesAtSpeeds(_4205.VirtualComponentCompoundModalAnalysesAtSpeeds):
    '''MeasurementComponentCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4037.MeasurementComponentModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4037.MeasurementComponentModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_4037.MeasurementComponentModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_4037.MeasurementComponentModalAnalysesAtSpeeds))
        return value
