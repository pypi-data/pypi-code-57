'''_1465.py

BearingLoadCaseResultsLightweight
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT = python_net_import('SMT.MastaAPI.Bearings', 'BearingLoadCaseResultsLightweight')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCaseResultsLightweight',)


class BearingLoadCaseResultsLightweight(_1.APIBase):
    '''BearingLoadCaseResultsLightweight

    This is a mastapy class.
    '''

    TYPE = _BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingLoadCaseResultsLightweight.TYPE'):
        super().__init__(instance_to_wrap)
