from django.db import models
from django.utils.functional import cached_property
from django.http import HttpResponse
from django.conf import settings
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.utils import camelcase_to_underscore

from webspace.cms.amp.mixins import AmpMixin
from webspace.cms.amp.utils import amp_mode_active
from webspace.cms import constants
from webspace.cms.blocks.schemas import HowTo, FAQPage
from webspace.cms.blocks.common import ButtonBlock
from webspace.loader import get_model, get_class

#  Classes

ArticlesEntry = get_class('cms.blocks.entries', 'ArticlesEntry')
ButtonsEntry = get_class('cms.blocks.entries', 'ButtonsEntry')
CardsEntry = get_class('cms.blocks.entries', 'CardsEntry')
EmbedEntry = get_class('cms.blocks.entries', 'EmbedEntry')
FirstContentEntry = get_class('cms.blocks.entries', 'FirstContentEntry')
GridInfoEntry = get_class('cms.blocks.entries', 'GridInfoEntry')
ImageEntry = get_class('cms.blocks.entries', 'ImageEntry')
MediaTextEntry = get_class('cms.blocks.entries', 'MediaTextEntry')
MediasLineEntry = get_class('cms.blocks.entries', 'MediasLineEntry')
SvgEntry = get_class('cms.blocks.entries', 'SvgEntry')
TextEntry = get_class('cms.blocks.entries', 'TextEntry')
TimeLineEntry = get_class('cms.blocks.entries', 'TimeLineEntry')
CalendlyEntry = get_class('cms.blocks.entries', 'CalendlyEntry')
SocialShare = get_class('cms.blocks.static', 'SocialShare')


#  Models
Menu = get_model('cms', 'Menu')
IconSnippet = get_model('cms', 'IconSnippet')


class AGenericPage(Page):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="SEO - Image",
    )

    theme = models.CharField(
        choices=constants.THEME_CHOICES,
        default=constants.THEME_SPACE,
        max_length=100,
        help_text="Permet de changer le theme du header et du footer"
    )

    breadcrumb = models.BooleanField(
        default=True,
        verbose_name="Public pour Google",
        help_text="Ajoute la page dans le sitemap et génère un schéma Breadcrumb",
    )

    header_menus = StreamField([
        ('menu', SnippetChooserBlock(Menu, required=False)),
    ], blank=True)

    header_buttons = StreamField([
        ('button', ButtonBlock())
    ], blank=True)

    schemas = StreamField([
        ('how_to', HowTo()),
        ('faq_page', FAQPage()),
    ], blank=True)

    body = StreamField([
        ('first_content', FirstContentEntry()),
        ('svg', SvgEntry()),
        ('image', ImageEntry()),
        ('text', TextEntry()),
        ('cards', CardsEntry()),
        ('media_text', MediaTextEntry()),
        ('grid_info', GridInfoEntry()),
        ('medias_line', MediasLineEntry()),
        ('timeline', TimeLineEntry()),
        ('buttons', ButtonsEntry()),
        ('calendly', CalendlyEntry()),
        ('articles', ArticlesEntry()),
        ('embed', EmbedEntry()),
        ('social_share', SocialShare())
    ], blank=True)

    footer = StreamField([
        ('menu', SnippetChooserBlock(Menu, required=False)),
    ], blank=True)

    content_panels = [
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], "Google Search"),
        MultiFieldPanel([
            ImageChooserPanel('feed_image'),
            FieldPanel('breadcrumb'),
        ], "SEO - DATA"),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('theme'),
        StreamFieldPanel('header_menus'),
        StreamFieldPanel('header_buttons'),
        StreamFieldPanel('footer'),
    ]

    subpage_types = [
        'cms.ContentPage',
        'cms.DocumentPage',
    ]

    class Meta:
        abstract = True
        app_label = 'cms'

    def get_context(self, request, *args, **kwargs):
        context = super(AGenericPage, self).get_context(request)
        context['debug'] = str(settings.DEBUG)
        context['icons'] = IconSnippet.get_context()
        return context

    @cached_property
    def get_breadcrumbs(self):
        #  FIXME: filter by `breadcrumb` seem not to be possible with wagtail Page
        ret = []
        items = self.get_children().type(AGenericPage).specific().live()
        for item in items:
            if item.breadcrumb:
                ret.append(item)
        return ret

    def get_sitemap_urls(self, request=None):
        if not self.breadcrumb:
            return []
        return super().get_sitemap_urls(request)

    def get_url_parts(self, *args, **kwargs):
        urls = super().get_url_parts(*args, **kwargs)
        if isinstance(self, AmpMixin) and amp_mode_active():
            return (urls[0], urls[1], '/amp' + urls[2])
        return urls

    def render_baked_file(self, request, path_file):
        index = 'index.html' if request.user_agent.is_pc else 'index-mobile.html'
        if amp_mode_active():
            index = index.replace('.html', '-amp.html')
            path_file = path_file.replace('/amp', '')
        with open(path_file + index, "rb") as fd:
            compressed = fd.read()
            response = HttpResponse(compressed)
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = str(len(compressed))
            return response

    def get_template(self, request, *args, **kwargs):
        return "%s/%s.html" % (
            constants.PAGES_TEMPLATES_PATH,
            camelcase_to_underscore(self.__class__.__name__)
        )
