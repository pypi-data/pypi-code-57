'''_3291.py

BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3289
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis',)


class BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis(_3289.BevelDifferentialGearCompoundSingleMeshWhineAnalysis):
    '''BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
