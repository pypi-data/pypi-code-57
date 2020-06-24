'''_6092.py

CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6089
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis',)


class CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis(_6089.CylindricalGearCompoundMultiBodyDynamicsAnalysis):
    '''CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
