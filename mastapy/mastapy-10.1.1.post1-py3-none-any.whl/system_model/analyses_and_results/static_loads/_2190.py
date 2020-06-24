'''_2190.py

RollingRingLoadCase
'''


from mastapy.system_model.part_model.couplings import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2180
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingLoadCase',)


class RollingRingLoadCase(_2180.CouplingHalfLoadCase):
    '''RollingRingLoadCase

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2018.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
