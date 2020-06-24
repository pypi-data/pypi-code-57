'''_5703.py

CVTBeltConnectionCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5672
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CVTBeltConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundGearWhineAnalysis',)


class CVTBeltConnectionCompoundGearWhineAnalysis(_5672.BeltConnectionCompoundGearWhineAnalysis):
    '''CVTBeltConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
