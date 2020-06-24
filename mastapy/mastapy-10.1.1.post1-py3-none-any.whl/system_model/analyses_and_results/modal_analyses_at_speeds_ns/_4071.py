'''_4071.py

StraightBevelGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6188
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3981
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearModalAnalysesAtSpeeds',)


class StraightBevelGearModalAnalysesAtSpeeds(_3981.BevelGearModalAnalysesAtSpeeds):
    '''StraightBevelGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2086.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6188.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6188.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
