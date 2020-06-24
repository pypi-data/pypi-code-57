'''_2862.py

SpecialisedAssemblyCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2840
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SpecialisedAssemblyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundGearWhineAnalysis',)


class SpecialisedAssemblyCompoundGearWhineAnalysis(_2840.AbstractAssemblyCompoundGearWhineAnalysis):
    '''SpecialisedAssemblyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
