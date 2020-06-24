'''_1484.py

ElementPropertiesWithMaterial
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _1476
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_WITH_MATERIAL = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesWithMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesWithMaterial',)


class ElementPropertiesWithMaterial(_1476.ElementPropertiesBase):
    '''ElementPropertiesWithMaterial

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_WITH_MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesWithMaterial.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def material_id(self) -> 'list_with_selected_item.ListWithSelectedItem_int':
        '''list_with_selected_item.ListWithSelectedItem_int: 'MaterialID' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_int)(self.wrapped.MaterialID) if self.wrapped.MaterialID else None

    @material_id.setter
    def material_id(self, value: 'list_with_selected_item.ListWithSelectedItem_int.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.MaterialID = value
