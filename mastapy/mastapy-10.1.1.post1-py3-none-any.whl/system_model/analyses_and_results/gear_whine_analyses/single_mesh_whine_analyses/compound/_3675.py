'''_3675.py

StraightBevelSunGearCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3670
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'StraightBevelSunGearCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundSingleMeshWhineAnalysis',)


class StraightBevelSunGearCompoundSingleMeshWhineAnalysis(_3670.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis):
    '''StraightBevelSunGearCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
