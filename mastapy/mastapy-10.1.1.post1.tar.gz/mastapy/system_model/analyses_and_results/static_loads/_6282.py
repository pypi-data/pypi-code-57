'''_6282.py

ImportedFEWrapper
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WRAPPER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ImportedFEWrapper')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWrapper',)


class ImportedFEWrapper(_1.APIBase):
    '''ImportedFEWrapper

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WRAPPER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWrapper.TYPE'):
        super().__init__(instance_to_wrap)
