'''_5525.py

ZerolBevelGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2169
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5422
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ZerolBevelGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysisAtAStiffness',)


class ZerolBevelGearModalAnalysisAtAStiffness(_5422.BevelGearModalAnalysisAtAStiffness):
    '''ZerolBevelGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2169.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2169.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
