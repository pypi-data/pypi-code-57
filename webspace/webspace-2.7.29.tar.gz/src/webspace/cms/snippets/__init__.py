from wagtail.snippets.models import register_snippet
from .icon import AIconSnippet
from ...loader import is_model_registered


if not is_model_registered('cms', 'IconSnippet'):
    @register_snippet
    class IconSnippet(AIconSnippet):
        pass


    # __all__.append('IconSnippet')

from .menu import AMenu, AMenuItem

if not is_model_registered('cms', 'Menu'):
    @register_snippet
    class Menu(AMenu):
        pass


    # __all__.append('Menu')

if not is_model_registered('cms', 'MenuItem'):
    class MenuItem(AMenuItem):
        pass


    # __all__.append('MenuItem')

from .svg import ASvg

if not is_model_registered('cms', 'Svg'):
    @register_snippet
    class Svg(ASvg):
        pass


    # __all__.append('Svg')
