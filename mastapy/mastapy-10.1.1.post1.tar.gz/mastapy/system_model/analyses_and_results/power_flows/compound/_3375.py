'''_3375.py

ConnectionCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6485
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundPowerFlow',)


class ConnectionCompoundPowerFlow(_6485.ConnectionCompoundAnalysis):
    '''ConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
