'''_1856.py

FEExportSettings
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_EXPORT_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'FEExportSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('FEExportSettings',)


class FEExportSettings(_1.APIBase):
    '''FEExportSettings

    This is a mastapy class.
    '''

    TYPE = _FE_EXPORT_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEExportSettings.TYPE'):
        super().__init__(instance_to_wrap)
