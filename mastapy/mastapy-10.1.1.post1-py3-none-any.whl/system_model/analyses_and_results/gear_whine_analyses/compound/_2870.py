'''_2870.py

AGMAGleasonConicalGearCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2878
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'AGMAGleasonConicalGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearCompoundGearWhineAnalysis',)


class AGMAGleasonConicalGearCompoundGearWhineAnalysis(_2878.ConicalGearCompoundGearWhineAnalysis):
    '''AGMAGleasonConicalGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
