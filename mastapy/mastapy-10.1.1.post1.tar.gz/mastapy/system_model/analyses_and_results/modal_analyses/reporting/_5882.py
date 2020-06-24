'''_5882.py

CalculateFullFEResultsForMode
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _5900
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CALCULATE_FULL_FE_RESULTS_FOR_MODE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'CalculateFullFEResultsForMode')


__docformat__ = 'restructuredtext en'
__all__ = ('CalculateFullFEResultsForMode',)


class CalculateFullFEResultsForMode(_1.APIBase):
    '''CalculateFullFEResultsForMode

    This is a mastapy class.
    '''

    TYPE = _CALCULATE_FULL_FE_RESULTS_FOR_MODE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CalculateFullFEResultsForMode.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def fe_results(self) -> 'List[_5900.ModalCMSResultsForModeAndFE]':
        '''List[ModalCMSResultsForModeAndFE]: 'FEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEResults, constructor.new(_5900.ModalCMSResultsForModeAndFE))
        return value
