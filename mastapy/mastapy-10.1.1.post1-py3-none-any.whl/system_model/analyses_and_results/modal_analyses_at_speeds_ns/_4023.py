'''_4023.py

HypoidGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6133
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3969
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'HypoidGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearModalAnalysesAtSpeeds',)


class HypoidGearModalAnalysesAtSpeeds(_3969.AGMAGleasonConicalGearModalAnalysesAtSpeeds):
    '''HypoidGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2073.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6133.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6133.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
