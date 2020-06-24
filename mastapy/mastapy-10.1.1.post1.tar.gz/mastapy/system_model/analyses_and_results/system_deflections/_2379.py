'''_2379.py

LoadSharingFactorReporter
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOAD_SHARING_FACTOR_REPORTER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'LoadSharingFactorReporter')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadSharingFactorReporter',)


class LoadSharingFactorReporter(_1.APIBase):
    '''LoadSharingFactorReporter

    This is a mastapy class.
    '''

    TYPE = _LOAD_SHARING_FACTOR_REPORTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadSharingFactorReporter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_sharing_factor(self) -> 'float':
        '''float: 'LoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadSharingFactor
