'''_6167.py

PulleyLoadCase
'''


from mastapy.system_model.part_model.couplings import _2124
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6086
from mastapy._internal.python_net import python_net_import

_PULLEY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PulleyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyLoadCase',)


class PulleyLoadCase(_6086.CouplingHalfLoadCase):
    '''PulleyLoadCase

    This is a mastapy class.
    '''

    TYPE = _PULLEY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2124.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2124.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
