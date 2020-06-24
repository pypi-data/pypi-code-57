'''_4942.py

StraightBevelDiffGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2084
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4805
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4859
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'StraightBevelDiffGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundModalAnalysis',)


class StraightBevelDiffGearCompoundModalAnalysis(_4859.BevelGearCompoundModalAnalysis):
    '''StraightBevelDiffGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4805.StraightBevelDiffGearModalAnalysis]':
        '''List[StraightBevelDiffGearModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4805.StraightBevelDiffGearModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4805.StraightBevelDiffGearModalAnalysis]':
        '''List[StraightBevelDiffGearModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4805.StraightBevelDiffGearModalAnalysis))
        return value
