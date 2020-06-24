'''_6275.py

GearSetHarmonicLoadData
'''


from typing import List

from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _2262, _6274, _6237
from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1006
from mastapy._internal.python_net import python_net_import

_GEAR_SET_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GearSetHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetHarmonicLoadData',)


class GearSetHarmonicLoadData(_6237.HarmonicLoadDataBase):
    '''GearSetHarmonicLoadData

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_HARMONIC_LOAD_DATA
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_mesh(self) -> 'list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase: 'GearMesh' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @gear_mesh.setter
    def gear_mesh(self, value: 'list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearMeshLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.GearMesh = value

    @property
    def gear_mesh_te_order_type(self) -> '_6274.GearMeshTEOrderType':
        '''GearMeshTEOrderType: 'GearMeshTEOrderType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearMeshTEOrderType)
        return constructor.new(_6274.GearMeshTEOrderType)(value) if value else None

    @gear_mesh_te_order_type.setter
    def gear_mesh_te_order_type(self, value: '_6274.GearMeshTEOrderType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearMeshTEOrderType = value

    @property
    def excitation_order_as_rotational_order_of_shaft(self) -> 'float':
        '''float: 'ExcitationOrderAsRotationalOrderOfShaft' is the original name of this property.'''

        return self.wrapped.ExcitationOrderAsRotationalOrderOfShaft

    @excitation_order_as_rotational_order_of_shaft.setter
    def excitation_order_as_rotational_order_of_shaft(self, value: 'float'):
        self.wrapped.ExcitationOrderAsRotationalOrderOfShaft = float(value) if value else 0.0

    @property
    def reference_shaft(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'ReferenceShaft' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.ReferenceShaft) if self.wrapped.ReferenceShaft else None

    @reference_shaft.setter
    def reference_shaft(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.ReferenceShaft = value

    @property
    def excitations(self) -> 'List[_1006.FourierSeries]':
        '''List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Excitations, constructor.new(_1006.FourierSeries))
        return value
