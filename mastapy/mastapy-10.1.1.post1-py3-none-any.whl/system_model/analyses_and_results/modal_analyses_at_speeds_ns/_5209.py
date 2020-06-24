'''_5209.py

CylindricalGearModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2326
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5220
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CylindricalGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearModalAnalysesAtSpeeds',)


class CylindricalGearModalAnalysesAtSpeeds(_5220.GearModalAnalysesAtSpeeds):
    '''CylindricalGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2326.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2326.CylindricalGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearModalAnalysesAtSpeeds]':
        '''List[CylindricalGearModalAnalysesAtSpeeds]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearModalAnalysesAtSpeeds))
        return value
