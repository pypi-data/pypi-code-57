'''_2266.py

BoltLoadCase
'''


from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2268
from mastapy._internal.python_net import python_net_import

_BOLT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BoltLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltLoadCase',)


class BoltLoadCase(_2268.ComponentLoadCase):
    '''BoltLoadCase

    This is a mastapy class.
    '''

    TYPE = _BOLT_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
