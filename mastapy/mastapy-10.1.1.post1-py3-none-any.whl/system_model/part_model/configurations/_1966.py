'''_1966.py

ActiveImportedFESelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2061, _2077
from mastapy.system_model.part_model import _1924
from mastapy.system_model.imported_fes import _99
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelectionGroup',)


class ActiveImportedFESelectionGroup(_2061.PartDetailConfiguration['_2077.ActiveImportedFESelection', '_1924.ImportedFEComponent', '_99.ImportedFE']):
    '''ActiveImportedFESelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
