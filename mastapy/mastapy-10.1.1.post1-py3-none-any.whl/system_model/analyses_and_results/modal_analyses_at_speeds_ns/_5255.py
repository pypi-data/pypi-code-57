'''_5255.py

ShaftModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2306
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5168
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ShaftModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalAnalysesAtSpeeds',)


class ShaftModalAnalysesAtSpeeds(_5168.AbstractShaftOrHousingModalAnalysesAtSpeeds):
    '''ShaftModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2306.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2306.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftModalAnalysesAtSpeeds]':
        '''List[ShaftModalAnalysesAtSpeeds]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftModalAnalysesAtSpeeds))
        return value
