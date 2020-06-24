'''_5272.py

TimeSeriesLoadCase
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5987
from mastapy.system_model.analyses_and_results.static_loads import _5891
from mastapy._internal.python_net import python_net_import

_TIME_SERIES_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TimeSeriesLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('TimeSeriesLoadCase',)


class TimeSeriesLoadCase(_5891.LoadCase):
    '''TimeSeriesLoadCase

    This is a mastapy class.
    '''

    TYPE = _TIME_SERIES_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TimeSeriesLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duration_for_rating(self) -> 'float':
        '''float: 'DurationForRating' is the original name of this property.'''

        return self.wrapped.DurationForRating

    @duration_for_rating.setter
    def duration_for_rating(self, value: 'float'):
        self.wrapped.DurationForRating = float(value) if value else 0.0

    @property
    def driva_analysis_options(self) -> '_5987.MBDAnalysisOptions':
        '''MBDAnalysisOptions: 'DRIVAAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5987.MBDAnalysisOptions)(self.wrapped.DRIVAAnalysisOptions) if self.wrapped.DRIVAAnalysisOptions else None
