'''_2938.py

CouplingConnectionCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2932
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CouplingConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundGearWhineAnalysis',)


class CouplingConnectionCompoundGearWhineAnalysis(_2932.InterMountableComponentConnectionCompoundGearWhineAnalysis):
    '''CouplingConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
