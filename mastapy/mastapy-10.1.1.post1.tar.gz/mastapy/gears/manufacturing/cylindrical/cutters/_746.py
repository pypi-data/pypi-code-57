'''_746.py

CustomisableEdgeProfile
'''


from typing import List

from mastapy.gears.manufacturing.cylindrical.cutters import _759
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CUSTOMISABLE_EDGE_PROFILE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CustomisableEdgeProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomisableEdgeProfile',)


class CustomisableEdgeProfile(_1.APIBase):
    '''CustomisableEdgeProfile

    This is a mastapy class.
    '''

    TYPE = _CUSTOMISABLE_EDGE_PROFILE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomisableEdgeProfile.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def customised_cutting_edge_profile(self) -> 'List[_759.MutatableCommon]':
        '''List[MutatableCommon]: 'CustomisedCuttingEdgeProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CustomisedCuttingEdgeProfile, constructor.new(_759.MutatableCommon))
        return value
