'''_2147.py

ActiveShaftDesignSelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2150, _2146
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.shafts import _40
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelectionGroup',)


class ActiveShaftDesignSelectionGroup(_2150.PartDetailConfiguration['_2146.ActiveShaftDesignSelection', '_2022.Shaft', '_40.SimpleShaftDefinition']):
    '''ActiveShaftDesignSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
