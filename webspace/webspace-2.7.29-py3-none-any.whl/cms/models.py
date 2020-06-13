from ..loader import is_model_registered

# __all__ = []

# Snippets

from .snippets import *


#  Pages


from .pages._generic import AGenericPage

if not is_model_registered('cms', 'GenericPage'):
    class GenericPage(AGenericPage):
        pass


    # __all__.append('GenericPage')

from .pages.blog import ABlogIndexPage, ABlogPage, ABlogPageTag

if not is_model_registered('cms', 'BlogPageTag'):
    class BlogPageTag(ABlogPageTag):
        pass


    # __all__.append('BlogPageTag')

if not is_model_registered('cms', 'BlogIndexPage'):
    class BlogIndexPage(ABlogIndexPage):
        pass


    # __all__.append('BlogIndexPage')

if not is_model_registered('cms', 'BlogPage'):
    class BlogPage(ABlogPage):
        pass


    # __all__.append('BlogPage')

from .pages.content import AContentPage

if not is_model_registered('cms', 'ContentPage'):
    class ContentPage(AContentPage):
        pass


    # __all__.append('ContentPage')

from .pages.home import AHomePage

if not is_model_registered('cms', 'HomePage'):
    class HomePage(AHomePage):
        pass


    # __all__.append('HomePage')

from .pages.document import ADocumentPage

if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass


    # __all__.append('DocumentPage')

#  Settings


from .settings.social_media import ASocialMediaSettings

if not is_model_registered('cms', 'SocialMediaSettings'):
    class SocialMediaSettings(ASocialMediaSettings):
        pass


    # __all__.append('SocialMediaSettings')

from .settings.theme import AThemeSettings

if not is_model_registered('cms', 'ThemeSettings'):
    class ThemeSettings(AThemeSettings):
        pass


    # __all__.append('ThemeSettings')

from .settings.content import AContentSettings

if not is_model_registered('cms', 'ContentSettings'):
    class ContentSettings(AContentSettings):
        pass


    # __all__.append('ContentSettings')
