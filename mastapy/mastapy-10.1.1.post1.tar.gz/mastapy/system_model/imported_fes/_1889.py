'''_1889.py

RaceBearingFE
'''


from typing import Callable, List

from mastapy.system_model.imported_fes import _1836, _1842
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _1916
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'RaceBearingFE')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFE',)


class RaceBearingFE(_1.APIBase):
    '''RaceBearingFE

    This is a mastapy class.
    '''

    TYPE = _RACE_BEARING_FE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceBearingFE.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def alignment_method(self) -> '_1836.AlignmentMethodForRaceBearing':
        '''AlignmentMethodForRaceBearing: 'AlignmentMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AlignmentMethod)
        return constructor.new(_1836.AlignmentMethodForRaceBearing)(value) if value else None

    @alignment_method.setter
    def alignment_method(self, value: '_1836.AlignmentMethodForRaceBearing'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def fe_filename(self) -> 'str':
        '''str: 'FEFilename' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEFilename

    @property
    def import_fe_mesh(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportFEMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportFEMesh

    @property
    def find_nodes_for_links(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'FindNodesForLinks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FindNodesForLinks

    @property
    def datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        '''list_with_selected_item.ListWithSelectedItem_Datum: 'Datum' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Datum)(self.wrapped.Datum) if self.wrapped.Datum else None

    @datum.setter
    def datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Datum = value

    @property
    def copy_datum_to_manual(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CopyDatumToManual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CopyDatumToManual

    @property
    def links(self) -> 'List[_1842.BearingRaceNodeLink]':
        '''List[BearingRaceNodeLink]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Links, constructor.new(_1842.BearingRaceNodeLink))
        return value
