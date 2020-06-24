'''_2152.py

CompoundAnalysis
'''


from typing import Iterable

from mastapy._internal import constructor, conversion
from mastapy import _6501
from mastapy.system_model import _1795
from mastapy.system_model.analyses_and_results.analysis_cases import _6489
from mastapy._internal.python_net import python_net_import

_COMPOUND_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundAnalysis',)


class CompoundAnalysis:
    '''CompoundAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundAnalysis.TYPE'):
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

    def perform_analysis_with_progress(self, progress: '_6501.TaskProgress'):
        ''' 'PerformAnalysis' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        '''

        self.wrapped.PerformAnalysis(progress.wrapped if progress else None)

    def results_for(self, design_entity: '_1795.DesignEntity') -> 'Iterable[_6489.DesignEntityCompoundAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.analysis_cases.DesignEntityCompoundAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6489.DesignEntityCompoundAnalysis))

    def initialize_lifetime_service(self) -> 'object':
        ''' 'InitializeLifetimeService' is the original name of this method.

        Returns:
            object
        '''

        method_result = self.wrapped.InitializeLifetimeService()
        return method_result
