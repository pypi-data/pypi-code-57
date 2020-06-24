'''_6496.py

StaticLoadAnalysisCase
'''


from mastapy.system_model.analyses_and_results.static_loads import _6184
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _6481
from mastapy._internal.python_net import python_net_import

_STATIC_LOAD_ANALYSIS_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'StaticLoadAnalysisCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticLoadAnalysisCase',)


class StaticLoadAnalysisCase(_6481.AnalysisCase):
    '''StaticLoadAnalysisCase

    This is a mastapy class.
    '''

    TYPE = _STATIC_LOAD_ANALYSIS_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StaticLoadAnalysisCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_case(self) -> '_6184.StaticLoadCase':
        '''StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.StaticLoadCase)(self.wrapped.LoadCase) if self.wrapped.LoadCase else None
