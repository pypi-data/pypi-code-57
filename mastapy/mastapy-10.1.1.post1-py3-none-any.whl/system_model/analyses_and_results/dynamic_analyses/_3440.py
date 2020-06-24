'''_3440.py

ExternalCADModelDynamicAnalysis
'''


from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2315
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3437
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ExternalCADModelDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelDynamicAnalysis',)


class ExternalCADModelDynamicAnalysis(_3437.ComponentDynamicAnalysis):
    '''ExternalCADModelDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2315.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
