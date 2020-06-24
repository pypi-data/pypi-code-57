'''_3942.py

StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2084
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3822
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3859
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses',)


class StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses(_3859.BevelGearCompoundModalAnalysesAtStiffnesses):
    '''StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3822.StraightBevelDiffGearModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3822.StraightBevelDiffGearModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3822.StraightBevelDiffGearModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3822.StraightBevelDiffGearModalAnalysesAtStiffnesses))
        return value
