'''_6228.py

GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_LOCATION_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic',)


class GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic(_1.APIBase):
    '''GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_LOCATION_WITHIN_A_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
