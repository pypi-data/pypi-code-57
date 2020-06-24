'''_1839.py

BaseFEWithSelection
'''


from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import (
    _200, _174, _199, _181
)
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BASE_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BaseFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BaseFEWithSelection',)


class BaseFEWithSelection(_1.APIBase):
    '''BaseFEWithSelection

    This is a mastapy class.
    '''

    TYPE = _BASE_FE_WITH_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BaseFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_selected_faces(self) -> 'int':
        '''int: 'NumberOfSelectedFaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfSelectedFaces

    @property
    def number_of_selected_nodes(self) -> 'int':
        '''int: 'NumberOfSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfSelectedNodes

    @property
    def selected_component(self) -> 'str':
        '''str: 'SelectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectedComponent

    @property
    def node_selection(self) -> '_200.FENodeSelectionDrawStyle':
        '''FENodeSelectionDrawStyle: 'NodeSelection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_200.FENodeSelectionDrawStyle)(self.wrapped.NodeSelection) if self.wrapped.NodeSelection else None

    @property
    def draw_style(self) -> '_174.DrawStyleForImportedFE':
        '''DrawStyleForImportedFE: 'DrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.DrawStyleForImportedFE)(self.wrapped.DrawStyle) if self.wrapped.DrawStyle else None

    @property
    def transparency_draw_style(self) -> '_199.FEModelTransparencyDrawStyle':
        '''FEModelTransparencyDrawStyle: 'TransparencyDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_199.FEModelTransparencyDrawStyle)(self.wrapped.TransparencyDrawStyle) if self.wrapped.TransparencyDrawStyle else None

    @property
    def component_draw_style(self) -> '_181.FEModelComponentDrawStyle':
        '''FEModelComponentDrawStyle: 'ComponentDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_181.FEModelComponentDrawStyle)(self.wrapped.ComponentDrawStyle) if self.wrapped.ComponentDrawStyle else None
