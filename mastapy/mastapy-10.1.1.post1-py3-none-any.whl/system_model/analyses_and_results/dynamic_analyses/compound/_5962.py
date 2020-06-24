'''_5962.py

CylindricalPlanetGearCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5959
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CylindricalPlanetGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundDynamicAnalysis',)


class CylindricalPlanetGearCompoundDynamicAnalysis(_5959.CylindricalGearCompoundDynamicAnalysis):
    '''CylindricalPlanetGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
