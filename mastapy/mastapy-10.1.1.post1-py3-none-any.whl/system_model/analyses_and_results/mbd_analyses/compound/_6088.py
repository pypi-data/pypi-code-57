'''_6088.py

CVTPulleyCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6127
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CVTPulleyCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundMultiBodyDynamicsAnalysis',)


class CVTPulleyCompoundMultiBodyDynamicsAnalysis(_6127.PulleyCompoundMultiBodyDynamicsAnalysis):
    '''CVTPulleyCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
