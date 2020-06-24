'''_1104.py

ConicalSetFEModel
'''


from mastapy.gears.fe_model.conical import _1122
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.gears.manufacturing.bevel import _810
from mastapy.gears.fe_model import _1102
from mastapy._internal.python_net import python_net_import

_CONICAL_SET_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel.Conical', 'ConicalSetFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalSetFEModel',)


class ConicalSetFEModel(_1102.GearSetFEModel):
    '''ConicalSetFEModel

    This is a mastapy class.
    '''

    TYPE = _CONICAL_SET_FE_MODEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalSetFEModel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank_data_source(self) -> '_1122.FlankDataSource':
        '''FlankDataSource: 'FlankDataSource' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FlankDataSource)
        return constructor.new(_1122.FlankDataSource)(value) if value else None

    @flank_data_source.setter
    def flank_data_source(self, value: '_1122.FlankDataSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FlankDataSource = value

    @property
    def selected_design(self) -> 'list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig':
        '''list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig: 'SelectedDesign' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig)(self.wrapped.SelectedDesign) if self.wrapped.SelectedDesign else None

    @selected_design.setter
    def selected_design(self, value: 'list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedDesign = value
