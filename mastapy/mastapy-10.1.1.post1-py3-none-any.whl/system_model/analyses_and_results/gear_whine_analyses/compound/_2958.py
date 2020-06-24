'''_2958.py

GearMeshCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2933
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'GearMeshCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundGearWhineAnalysis',)


class GearMeshCompoundGearWhineAnalysis(_2933.InterMountableComponentConnectionCompoundGearWhineAnalysis):
    '''GearMeshCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
