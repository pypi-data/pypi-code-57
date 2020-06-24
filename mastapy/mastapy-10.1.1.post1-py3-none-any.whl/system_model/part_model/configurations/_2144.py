'''_2144.py

ActiveImportedFESelection
'''


from mastapy.system_model.part_model.configurations import _2151
from mastapy.system_model.part_model import _2001
from mastapy.system_model.imported_fes import _1935
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelection',)


class ActiveImportedFESelection(_2151.PartDetailSelection['_2001.ImportedFEComponent', '_1935.ImportedFE']):
    '''ActiveImportedFESelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelection.TYPE'):
        super().__init__(instance_to_wrap)
