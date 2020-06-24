'''_2149.py

BearingDetailSelection
'''


from mastapy.system_model.part_model.configurations import _2151
from mastapy.system_model.part_model import _1985
from mastapy.bearings.bearing_designs import _1730
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailSelection',)


class BearingDetailSelection(_2151.PartDetailSelection['_1985.Bearing', '_1730.BearingDesign']):
    '''BearingDetailSelection

    This is a mastapy class.
    '''

    TYPE = _BEARING_DETAIL_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingDetailSelection.TYPE'):
        super().__init__(instance_to_wrap)
