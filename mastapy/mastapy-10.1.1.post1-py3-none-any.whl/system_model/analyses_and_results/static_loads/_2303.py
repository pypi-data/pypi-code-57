'''_2303.py

UnbalancedMassLoadCase
'''


from mastapy.system_model.part_model import _1938
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2305
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'UnbalancedMassLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassLoadCase',)


class UnbalancedMassLoadCase(_2305.VirtualComponentLoadCase):
    '''UnbalancedMassLoadCase

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
