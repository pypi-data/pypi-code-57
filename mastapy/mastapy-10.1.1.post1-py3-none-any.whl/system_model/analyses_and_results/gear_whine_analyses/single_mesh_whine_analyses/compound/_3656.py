'''_3656.py

CylindricalPlanetGearCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3654
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'CylindricalPlanetGearCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundSingleMeshWhineAnalysis',)


class CylindricalPlanetGearCompoundSingleMeshWhineAnalysis(_3654.CylindricalGearCompoundSingleMeshWhineAnalysis):
    '''CylindricalPlanetGearCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
