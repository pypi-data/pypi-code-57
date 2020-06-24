'''_5582.py

GearCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5602
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'GearCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundSingleMeshWhineAnalysis',)


class GearCompoundSingleMeshWhineAnalysis(_5602.MountableComponentCompoundSingleMeshWhineAnalysis):
    '''GearCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
