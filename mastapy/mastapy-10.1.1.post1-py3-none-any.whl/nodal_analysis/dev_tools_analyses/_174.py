'''_174.py

DrawStyleForImportedFE
'''


from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _86
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DRAW_STYLE_FOR_IMPORTED_FE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'DrawStyleForImportedFE')


__docformat__ = 'restructuredtext en'
__all__ = ('DrawStyleForImportedFE',)


class DrawStyleForImportedFE(_1.APIBase):
    '''DrawStyleForImportedFE

    This is a mastapy class.
    '''

    TYPE = _DRAW_STYLE_FOR_IMPORTED_FE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DrawStyleForImportedFE.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def node_size(self) -> 'int':
        '''int: 'NodeSize' is the original name of this property.'''

        return self.wrapped.NodeSize

    @node_size.setter
    def node_size(self, value: 'int'):
        self.wrapped.NodeSize = int(value) if value else 0

    @property
    def line_option(self) -> '_86.FEMeshElementEntityOption':
        '''FEMeshElementEntityOption: 'LineOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.LineOption)
        return constructor.new(_86.FEMeshElementEntityOption)(value) if value else None

    @line_option.setter
    def line_option(self, value: '_86.FEMeshElementEntityOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LineOption = value

    @property
    def grounded_nodes(self) -> 'bool':
        '''bool: 'GroundedNodes' is the original name of this property.'''

        return self.wrapped.GroundedNodes

    @grounded_nodes.setter
    def grounded_nodes(self, value: 'bool'):
        self.wrapped.GroundedNodes = bool(value) if value else False

    @property
    def rigid_elements(self) -> 'bool':
        '''bool: 'RigidElements' is the original name of this property.'''

        return self.wrapped.RigidElements

    @rigid_elements.setter
    def rigid_elements(self, value: 'bool'):
        self.wrapped.RigidElements = bool(value) if value else False

    @property
    def highlight_bad_elements(self) -> 'bool':
        '''bool: 'HighlightBadElements' is the original name of this property.'''

        return self.wrapped.HighlightBadElements

    @highlight_bad_elements.setter
    def highlight_bad_elements(self, value: 'bool'):
        self.wrapped.HighlightBadElements = bool(value) if value else False
