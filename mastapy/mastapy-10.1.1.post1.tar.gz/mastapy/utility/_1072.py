'''_1072.py

CachedIndependentReportablePropertiesBase
'''


from typing import Generic, TypeVar

from mastapy.utility import _326
from mastapy._internal.python_net import python_net_import

_CACHED_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import('SMT.MastaAPI.Utility', 'CachedIndependentReportablePropertiesBase')


__docformat__ = 'restructuredtext en'
__all__ = ('CachedIndependentReportablePropertiesBase',)


T = TypeVar('T', bound='CachedIndependentReportablePropertiesBase')


class CachedIndependentReportablePropertiesBase(_326.IndependentReportablePropertiesBase['T'], Generic[T]):
    '''CachedIndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _CACHED_INDEPENDENT_REPORTABLE_PROPERTIES_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CachedIndependentReportablePropertiesBase.TYPE'):
        super().__init__(instance_to_wrap)
