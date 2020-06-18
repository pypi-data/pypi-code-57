from wagtail.contrib.settings.models import register_setting
from wagtail.snippets.models import register_snippet
from wagtail.documents.models import Document, AbstractDocument
from django.db import models

from webspace.loader import is_model_registered

__all__ = []


class MyDocument(AbstractDocument):
    #  Dimensions for SVG

    width = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        help_text="for SVG"
    )
    height = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        help_text="for SVG"
    )

    admin_form_fields = Document.admin_form_fields + (
        'width',
        'height'
    )

    def get_size(self):
        return '500x500'


__all__.append('MyDocument')


# Snippets

from .snippets.icon import AIconSnippet

if not is_model_registered('cms', 'IconSnippet'):
    @register_snippet
    class IconSnippet(AIconSnippet):
        pass


    __all__.append('IconSnippet')

from .snippets.menu import AMenu, AMenuItem

if not is_model_registered('cms', 'Menu'):
    @register_snippet
    class Menu(AMenu):
        pass


    __all__.append('Menu')

if not is_model_registered('cms', 'MenuItem'):
    class MenuItem(AMenuItem):
        pass


    __all__.append('MenuItem')

#  Pages


from .pages._generic import AGenericPage

if not is_model_registered('cms', 'GenericPage'):
    class GenericPage(AGenericPage):
        pass


    __all__.append('GenericPage')

from .pages.blog import ABlogIndexPage, ABlogPage, ABlogPageTag

if not is_model_registered('cms', 'BlogPageTag'):
    class BlogPageTag(ABlogPageTag):
        pass


    __all__.append('BlogPageTag')

if not is_model_registered('cms', 'BlogIndexPage'):
    class BlogIndexPage(ABlogIndexPage):
        pass


    __all__.append('BlogIndexPage')

if not is_model_registered('cms', 'BlogPage'):
    class BlogPage(ABlogPage):
        pass


    __all__.append('BlogPage')

from .pages.content import AContentPage

if not is_model_registered('cms', 'ContentPage'):
    class ContentPage(AContentPage):
        pass


    __all__.append('ContentPage')

from .pages.home import AHomePage

if not is_model_registered('cms', 'HomePage'):
    class HomePage(AHomePage):
        pass


    __all__.append('HomePage')

from .pages.document import ADocumentPage

if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass


    __all__.append('DocumentPage')

#  Settings

from .settings.webspace import AWebspaceSettings

if not is_model_registered('cms', 'WebspaceSettings'):
    @register_setting
    class WebspaceSettings(AWebspaceSettings):
        pass


    __all__.append('WebspaceSettings')
