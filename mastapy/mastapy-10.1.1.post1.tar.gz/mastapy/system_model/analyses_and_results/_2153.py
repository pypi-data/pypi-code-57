'''_2153.py

SingleAnalysis
'''


from mastapy._internal import constructor
from mastapy import _6501
from mastapy.system_model import _1795
from mastapy.system_model.analyses_and_results import _2181
from mastapy._internal.python_net import python_net_import

_SINGLE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SingleAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleAnalysis',)


class SingleAnalysis:
    '''SingleAnalysis

    This is a mastapy class.
    '''

    TYPE = _SINGLE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SingleAnalysis.TYPE'):
        self.wrapped = instance_to_wrap

    @property
    def results_ready(self) -> 'bool':
        '''bool: 'ResultsReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResultsReady

    def perform_analysis(self):
        ''' 'PerformAnalysis' is the original name of this method.'''

        self.wrapped.PerformAnalysis()

    def perform_analysis_with_progress(self, task_progress: '_6501.TaskProgress'):
        ''' 'PerformAnalysis' is the original name of this method.

        Args:
            task_progress (mastapy.TaskProgress)
        '''

        self.wrapped.PerformAnalysis(task_progress.wrapped if task_progress else None)

    def results_for(self, design_entity: '_1795.DesignEntity') -> '_2181.DesignEntityAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)

        Returns:
            mastapy.system_model.analyses_and_results.DesignEntityAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2181.DesignEntityAnalysis)(method_result) if method_result else None

    def results_for_design_entity_analysis(self, design_entity_analysis: '_2181.DesignEntityAnalysis') -> '_2181.DesignEntityAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.DesignEntityAnalysis)

        Returns:
            mastapy.system_model.analyses_and_results.DesignEntityAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2181.DesignEntityAnalysis)(method_result) if method_result else None

    def initialize_lifetime_service(self) -> 'object':
        ''' 'InitializeLifetimeService' is the original name of this method.

        Returns:
            object
        '''

        method_result = self.wrapped.InitializeLifetimeService()
        return method_result
