'''_3693.py

PowerLoadDynamicAnalysis
'''


from mastapy.system_model.part_model import _1934
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2297
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3697
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PowerLoadDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadDynamicAnalysis',)


class PowerLoadDynamicAnalysis(_3697.VirtualComponentDynamicAnalysis):
    '''PowerLoadDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2297.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2297.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
