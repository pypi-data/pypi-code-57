'''_3044.py

SpecialisedAssemblyCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3022
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SpecialisedAssemblyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundModalAnalysis',)


class SpecialisedAssemblyCompoundModalAnalysis(_3022.AbstractAssemblyCompoundModalAnalysis):
    '''SpecialisedAssemblyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
