'''_2693.py

BevelGearSetCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2687
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BevelGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetCompoundDynamicAnalysis',)


class BevelGearSetCompoundDynamicAnalysis(_2687.AGMAGleasonConicalGearSetCompoundDynamicAnalysis):
    '''BevelGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
