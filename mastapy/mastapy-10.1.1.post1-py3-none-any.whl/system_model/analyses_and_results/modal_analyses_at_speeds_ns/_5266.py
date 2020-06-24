'''_5266.py

StraightBevelDiffGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2357
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5182
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelDiffGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearModalAnalysesAtSpeeds',)


class StraightBevelDiffGearModalAnalysesAtSpeeds(_5182.BevelGearModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2357.StraightBevelDiffGearLoadCase':
        '''StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2357.StraightBevelDiffGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
