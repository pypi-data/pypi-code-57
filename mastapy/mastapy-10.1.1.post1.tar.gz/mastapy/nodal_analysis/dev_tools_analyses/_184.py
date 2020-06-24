'''_184.py

FEModelInstanceDrawStyle
'''


from mastapy.nodal_analysis.dev_tools_analyses import _174
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_MODEL_INSTANCE_DRAW_STYLE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FEModelInstanceDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('FEModelInstanceDrawStyle',)


class FEModelInstanceDrawStyle(_1.APIBase):
    '''FEModelInstanceDrawStyle

    This is a mastapy class.
    '''

    TYPE = _FE_MODEL_INSTANCE_DRAW_STYLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEModelInstanceDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def model_draw_style(self) -> '_174.DrawStyleForImportedFE':
        '''DrawStyleForImportedFE: 'ModelDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.DrawStyleForImportedFE)(self.wrapped.ModelDrawStyle) if self.wrapped.ModelDrawStyle else None
