'''_2989.py

AGMAGleasonConicalGearSetCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _2997
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AGMAGleasonConicalGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetCompoundModalAnalysis',)


class AGMAGleasonConicalGearSetCompoundModalAnalysis(_2997.ConicalGearSetCompoundModalAnalysis):
    '''AGMAGleasonConicalGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
