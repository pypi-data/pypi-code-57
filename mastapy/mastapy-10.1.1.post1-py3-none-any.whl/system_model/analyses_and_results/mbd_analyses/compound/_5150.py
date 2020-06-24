'''_5150.py

CVTCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5119
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CVTCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundMultiBodyDynamicsAnalysis',)


class CVTCompoundMultiBodyDynamicsAnalysis(_5119.BeltDriveCompoundMultiBodyDynamicsAnalysis):
    '''CVTCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
