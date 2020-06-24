'''_3705.py

ConnectionCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _3613
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ConnectionCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundSingleMeshWhineAnalysis',)


class ConnectionCompoundSingleMeshWhineAnalysis(_3613.ConnectionCompoundAnalysis):
    '''ConnectionCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
