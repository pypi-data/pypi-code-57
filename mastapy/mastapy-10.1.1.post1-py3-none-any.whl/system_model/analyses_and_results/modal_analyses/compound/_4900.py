'''_4900.py

HypoidGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4757
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4847
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'HypoidGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundModalAnalysis',)


class HypoidGearCompoundModalAnalysis(_4847.AGMAGleasonConicalGearCompoundModalAnalysis):
    '''HypoidGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2073.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4757.HypoidGearModalAnalysis]':
        '''List[HypoidGearModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4757.HypoidGearModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4757.HypoidGearModalAnalysis]':
        '''List[HypoidGearModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4757.HypoidGearModalAnalysis))
        return value
